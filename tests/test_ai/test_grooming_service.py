"""
Tests for AI grooming service functionality.
"""

import pytest
import json
from unittest.mock import Mock, patch
import requests

from src.ai.grooming_service import GroomingService, GroomingResult
from src.ai.config import AIConfig
from .golden_set import GOLDEN_SET_TESTS, get_basic_golden_set, validate_grooming_result


class TestGroomingService:
    """Test cases for the GroomingService class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = GroomingService()
    
    def test_service_initialization(self):
        """Test that GroomingService initializes correctly."""
        assert self.service is not None
        assert isinstance(self.service.config, AIConfig)
        assert hasattr(self.service, 'session')
    
    def test_empty_input_handling(self):
        """Test handling of empty or whitespace-only input."""
        result = self.service.groom_todo_list("")
        assert not result.success
        assert "Empty todo list" in result.error_message
        
        result = self.service.groom_todo_list("   \n\n  ")
        assert not result.success
        assert "Empty todo list" in result.error_message
    
    def test_basic_fallback_grooming(self):
        """Test basic fallback grooming functionality."""
        input_text = "buy milk\nget bread\nbuy milk\nclean house"
        result = self.service._basic_grooming_fallback(input_text)
        
        assert result.success
        assert result.fallback_used
        assert len(result.groomed_tasks) == 3  # Should remove duplicate
        
        task_titles = [task['title'] for task in result.groomed_tasks]
        assert "buy milk" in task_titles
        assert "get bread" in task_titles
        assert "clean house" in task_titles
    
    def test_formatted_tasks_output(self):
        """Test that formatted task output works correctly."""
        tasks = [
            {"title": "Buy groceries", "priority": "high", "notes": "Get organic"},
            {"title": "Walk dog", "priority": "medium", "notes": ""}
        ]
        result = GroomingResult(success=True, groomed_tasks=tasks)
        
        formatted = result.get_formatted_tasks()
        assert "1. Buy groceries [HIGH PRIORITY] (Get organic)" in formatted
        assert "2. Walk dog" in formatted
    
    def test_basic_deduplication(self):
        """Test basic deduplication functionality."""
        input_text = "task 1\ntask 2\ntask 1\ntask 3"
        result = self.service._basic_grooming_fallback(input_text)
        
        assert result.success
        assert len(result.groomed_tasks) == 3  # Should remove one duplicate
        task_titles = [task['title'] for task in result.groomed_tasks]
        assert task_titles.count("task 1") == 1
    
    def test_numbering_cleanup(self):
        """Test that existing numbering is cleaned up properly."""
        input_text = "1. buy milk\n2. get bread\n3. clean house"
        result = self.service._basic_grooming_fallback(input_text)
        
        assert result.success
        task_titles = [task['title'] for task in result.groomed_tasks]
        assert "buy milk" in task_titles  # Number should be removed
        assert "1. buy milk" not in task_titles


class TestAIMocking:
    """Test cases using mocked AI responses."""
    
    def setup_method(self):
        """Set up test fixtures with mocked config."""
        with patch.dict('os.environ', {'HF_API_KEY': 'test-key'}):
            self.service = GroomingService()
    
    @patch('requests.Session.post')
    def test_successful_huggingface_response(self, mock_post):
        """Test successful HuggingFace API response processing."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "generated_text": json.dumps({
                "groomed_tasks": [
                    {"title": "Buy groceries", "priority": "medium", "notes": "Get fresh vegetables"},
                    {"title": "Walk the dog", "priority": "high", "notes": "Morning walk"}
                ],
                "processing_notes": "Clarified tasks and set priorities",
                "suggestions": ["Consider grouping similar tasks"]
            })
        }]
        mock_post.return_value = mock_response
        
        result = self.service._groom_with_huggingface("buy stuff\nwalk dog")
        
        assert result.success
        assert len(result.groomed_tasks) == 2
        assert result.groomed_tasks[0]['title'] == "Buy groceries"
        assert result.processing_notes == "Clarified tasks and set priorities"
    
    @patch('requests.Session.post')
    def test_huggingface_api_timeout(self, mock_post):
        """Test handling of API timeout."""
        mock_post.side_effect = requests.Timeout("Request timeout")
        
        result = self.service._groom_with_huggingface("test task")
        
        # Should fall back to basic grooming if fallback is enabled
        if self.service.config.fallback_enabled:
            assert result.success
            assert result.fallback_used
        else:
            assert not result.success
    
    @patch('requests.Session.post')
    def test_huggingface_model_loading(self, mock_post):
        """Test handling of model loading (503 response)."""
        # First call returns 503 (model loading)
        mock_response_loading = Mock()
        mock_response_loading.status_code = 503
        
        # Second call succeeds
        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = [{
            "generated_text": json.dumps({
                "groomed_tasks": [{"title": "Test task", "priority": "medium"}],
                "processing_notes": "Task processed"
            })
        }]
        
        mock_post.side_effect = [mock_response_loading, mock_response_success]
        
        with patch('time.sleep'):  # Speed up test by mocking sleep
            result = self.service._groom_with_huggingface("test task")
        
        assert result.success
        assert len(result.groomed_tasks) == 1
    
    @patch('requests.Session.post')
    def test_malformed_json_response(self, mock_post):
        """Test handling of malformed JSON in AI response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "generated_text": "This is not valid JSON { incomplete"
        }]
        mock_post.return_value = mock_response
        
        result = self.service._groom_with_huggingface("test task")
        
        # Should fall back to basic grooming when JSON parsing fails
        if self.service.config.fallback_enabled:
            assert result.success
            assert result.fallback_used
        else:
            assert not result.success


class TestGoldenSetValidation:
    """Test cases using the golden set for validation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = GroomingService()
    
    @pytest.mark.parametrize("test_case", get_basic_golden_set())
    def test_basic_golden_set_fallback(self, test_case):
        """Test basic golden set cases with fallback grooming."""
        result = self.service.groom_todo_list(test_case["input"])
        validation = validate_grooming_result(test_case, result)
        
        # Log validation results for debugging
        if not validation["passed"]:
            print(f"Test {test_case['name']} failed:")
            for issue in validation["issues"]:
                print(f"  - {issue}")
        
        assert validation["passed"], f"Golden set test '{test_case['name']}' failed: {validation['issues']}"
    
    def test_all_golden_set_basic_requirements(self):
        """Test that all golden set cases meet basic requirements."""
        results = []
        
        for test_case in GOLDEN_SET_TESTS:
            result = self.service.groom_todo_list(test_case["input"])
            validation = validate_grooming_result(test_case, result)
            
            results.append({
                "name": test_case["name"],
                "passed": validation["passed"],
                "score": validation["score"],
                "max_score": validation["max_score"],
                "issues": validation["issues"]
            })
        
        # Calculate overall success rate
        passed_tests = [r for r in results if r["passed"]]
        success_rate = len(passed_tests) / len(results) if results else 0
        
        print(f"\nGolden Set Results:")
        print(f"Success Rate: {success_rate:.1%} ({len(passed_tests)}/{len(results)})")
        
        for result in results:
            status = "✓" if result["passed"] else "✗"
            print(f"{status} {result['name']}: {result['score']}/{result['max_score']}")
            if result["issues"]:
                for issue in result["issues"]:
                    print(f"    - {issue}")
        
        # We expect at least 70% success rate with fallback grooming
        assert success_rate >= 0.7, f"Golden set success rate too low: {success_rate:.1%}"


class TestGroomingResult:
    """Test cases for GroomingResult class."""
    
    def test_grooming_result_creation(self):
        """Test GroomingResult initialization."""
        result = GroomingResult(success=True, groomed_tasks=[])
        assert result.success
        assert result.groomed_tasks == []
        assert not result.fallback_used
        assert result.error_message is None
    
    def test_empty_formatted_tasks(self):
        """Test formatted tasks with empty task list."""
        result = GroomingResult(success=True, groomed_tasks=[])
        formatted = result.get_formatted_tasks()
        assert formatted == ""
    
    def test_formatted_tasks_with_priorities(self):
        """Test formatted tasks with various priority levels."""
        tasks = [
            {"title": "Urgent task", "priority": "high"},
            {"title": "Normal task", "priority": "medium"},
            {"title": "Low priority task", "priority": "low"}
        ]
        result = GroomingResult(success=True, groomed_tasks=tasks)
        formatted = result.get_formatted_tasks()
        
        assert "[HIGH PRIORITY]" in formatted
        assert "Urgent task" in formatted
        assert "Normal task" in formatted
        assert "Low priority task" in formatted
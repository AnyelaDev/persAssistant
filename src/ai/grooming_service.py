"""
AI-Powered ToDo List Grooming Service

Provides intelligent todo list optimization using various AI services.
"""

import json
import time
import logging
from typing import Dict, List, Optional, Tuple
import requests

from .config import AIConfig
from .prompts import get_grooming_prompt, select_prompt_type, PROMPT_VERSION

# Set up logging
logger = logging.getLogger(__name__)


class GroomingResult:
    """Result of todo list grooming operation."""
    
    def __init__(self, success: bool, groomed_tasks: List[Dict] = None, 
                 error_message: str = None, fallback_used: bool = False,
                 processing_notes: str = None, suggestions: List[str] = None):
        self.success = success
        self.groomed_tasks = groomed_tasks or []
        self.error_message = error_message
        self.fallback_used = fallback_used
        self.processing_notes = processing_notes
        self.suggestions = suggestions or []
    
    def get_formatted_tasks(self) -> str:
        """Get formatted task list as string for UI display."""
        if not self.groomed_tasks:
            return ""
        
        formatted_lines = []
        for i, task in enumerate(self.groomed_tasks, 1):
            title = task.get('title', 'Untitled task')
            priority = task.get('priority', 'medium')
            notes = task.get('notes', '')
            
            line = f"{i}. {title}"
            if priority in ['high', 'urgent']:
                line += " [HIGH PRIORITY]"
            if notes:
                line += f" ({notes})"
            
            formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)


class GroomingService:
    """Main service for AI-powered todo list grooming."""
    
    def __init__(self):
        self.config = AIConfig()
        self.session = requests.Session()
        
        # Validate configuration on startup
        is_valid, message = self.config.validate_configuration()
        if not is_valid:
            logger.error(f"AI configuration invalid: {message}")
        else:
            logger.info(f"AI configuration: {message}")
    
    def groom_todo_list(self, todo_list: str) -> GroomingResult:
        """
        Groom a todo list using AI services with fallback handling.
        
        Args:
            todo_list: Raw todo list text from user
            
        Returns:
            GroomingResult with processed tasks or error information
        """
        if not todo_list or not todo_list.strip():
            return GroomingResult(
                success=False,
                error_message="Empty todo list provided"
            )
        
        # Try AI services in priority order
        service = self.config.primary_service
        
        try:
            if service == "huggingface":
                return self._groom_with_huggingface(todo_list)
            elif service == "openai":
                return self._groom_with_openai(todo_list)
            elif service == "anthropic":
                return self._groom_with_anthropic(todo_list)
            else:
                # Fallback mode
                return self._basic_grooming_fallback(todo_list)
                
        except Exception as e:
            logger.error(f"Grooming service error: {e}")
            if self.config.fallback_enabled:
                return self._basic_grooming_fallback(todo_list)
            else:
                return GroomingResult(
                    success=False,
                    error_message=f"AI service error: {str(e)}"
                )
    
    def _groom_with_huggingface(self, todo_list: str) -> GroomingResult:
        """Groom todo list using HuggingFace Inference API."""
        if not self.config.has_hf_key:
            raise ValueError("HuggingFace API key not configured")
        
        # Select appropriate prompt
        prompt_type = select_prompt_type(todo_list)
        prompt = get_grooming_prompt(todo_list, prompt_type)
        
        url = f"{self.config.hf_base_url}{self.config.hf_model}"
        headers = {
            "Authorization": f"Bearer {self.config.hf_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1000,
                "temperature": 0.3,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        # Retry logic with exponential backoff
        for attempt in range(self.config.max_retries + 1):
            try:
                logger.info(f"HuggingFace API call attempt {attempt + 1}")
                
                response = self.session.post(
                    url, 
                    headers=headers, 
                    json=payload,
                    timeout=self.config.timeout
                )
                
                if response.status_code == 200:
                    return self._parse_ai_response(response.json(), "huggingface")
                elif response.status_code == 503:
                    # Model loading, wait and retry
                    if attempt < self.config.max_retries:
                        wait_time = self.config.retry_delay * (2 ** attempt if self.config.exponential_backoff else 1)
                        logger.info(f"Model loading, waiting {wait_time}s before retry")
                        time.sleep(wait_time)
                        continue
                else:
                    logger.error(f"HuggingFace API error: {response.status_code} - {response.text}")
                    break
                    
            except requests.RequestException as e:
                logger.error(f"Request error on attempt {attempt + 1}: {e}")
                if attempt < self.config.max_retries:
                    wait_time = self.config.retry_delay * (2 ** attempt if self.config.exponential_backoff else 1)
                    time.sleep(wait_time)
                    continue
                break
        
        # If we get here, all attempts failed - use fallback
        if self.config.fallback_enabled:
            return self._basic_grooming_fallback(todo_list)
        else:
            return GroomingResult(
                success=False,
                error_message="HuggingFace API unavailable"
            )
    
    def _groom_with_openai(self, todo_list: str) -> GroomingResult:
        """Placeholder for OpenAI integration (future enhancement)."""
        # TODO: Implement OpenAI API integration
        return GroomingResult(
            success=False,
            error_message="OpenAI integration not yet implemented"
        )
    
    def _groom_with_anthropic(self, todo_list: str) -> GroomingResult:
        """Placeholder for Anthropic/Claude integration (future enhancement)."""
        # TODO: Implement Anthropic API integration
        return GroomingResult(
            success=False,
            error_message="Anthropic integration not yet implemented"
        )
    
    def _parse_ai_response(self, response_data: any, service: str) -> GroomingResult:
        """Parse AI service response into GroomingResult."""
        try:
            # Handle different response formats
            if isinstance(response_data, list) and len(response_data) > 0:
                # HuggingFace typically returns a list
                response_text = response_data[0].get('generated_text', '')
            elif isinstance(response_data, dict):
                response_text = response_data.get('generated_text', str(response_data))
            else:
                response_text = str(response_data)
            
            # Try to extract JSON from the response
            json_response = self._extract_json_from_text(response_text)
            
            if json_response:
                groomed_tasks = json_response.get('groomed_tasks', [])
                processing_notes = json_response.get('processing_notes', '')
                suggestions = json_response.get('suggestions', [])
                
                # Validate task structure
                validated_tasks = []
                for task in groomed_tasks:
                    if isinstance(task, dict) and 'title' in task:
                        validated_tasks.append({
                            'title': task.get('title', '').strip(),
                            'priority': task.get('priority', 'medium'),
                            'notes': task.get('notes', ''),
                            'estimated_time': task.get('estimated_time', ''),
                            'source': task.get('source', '')
                        })
                
                if validated_tasks:
                    return GroomingResult(
                        success=True,
                        groomed_tasks=validated_tasks,
                        processing_notes=processing_notes,
                        suggestions=suggestions
                    )
            
            # If JSON parsing failed, fall back to basic processing
            logger.warning(f"Could not parse {service} response as JSON, using fallback")
            return self._basic_grooming_fallback_from_ai_text(response_text)
            
        except Exception as e:
            logger.error(f"Error parsing {service} response: {e}")
            return GroomingResult(
                success=False,
                error_message=f"Failed to parse {service} response"
            )
    
    def _extract_json_from_text(self, text: str) -> Optional[Dict]:
        """Extract JSON object from potentially messy AI response text."""
        text = text.strip()
        
        # Look for JSON object boundaries
        start_idx = text.find('{')
        end_idx = text.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_text = text[start_idx:end_idx + 1]
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                pass
        
        # Try parsing the whole text as JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None
    
    def _basic_grooming_fallback_from_ai_text(self, ai_text: str) -> GroomingResult:
        """Create basic grooming result from AI text that couldn't be parsed as JSON."""
        # Extract task-like lines from AI response
        lines = [line.strip() for line in ai_text.split('\n') if line.strip()]
        tasks = []
        
        for line in lines:
            # Look for numbered or bulleted items
            if any(line.startswith(prefix) for prefix in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '-', '*']):
                # Clean up the line
                clean_line = line
                for prefix in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '-', '*']:
                    if clean_line.startswith(prefix):
                        clean_line = clean_line[len(prefix):].strip()
                        break
                
                if clean_line:
                    tasks.append({
                        'title': clean_line,
                        'priority': 'medium',
                        'notes': 'AI-processed',
                        'estimated_time': '',
                        'source': 'AI response parsing'
                    })
        
        if tasks:
            return GroomingResult(
                success=True,
                groomed_tasks=tasks,
                processing_notes="AI response parsed without structured JSON",
                fallback_used=True
            )
        else:
            # Fall back to basic grooming
            return self._basic_grooming_fallback(ai_text)
    
    def _basic_grooming_fallback(self, todo_list: str) -> GroomingResult:
        """Basic grooming without AI: numbering, deduplication, basic formatting."""
        lines = [line.strip() for line in todo_list.split('\n') if line.strip()]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_lines = []
        for line in lines:
            line_lower = line.lower()
            if line_lower not in seen:
                seen.add(line_lower)
                unique_lines.append(line)
        
        # Create basic task objects
        tasks = []
        for i, line in enumerate(unique_lines, 1):
            # Remove existing numbering if present
            clean_line = line
            import re
            if re.match(r'^\d+\.?\s*', line):
                clean_line = re.sub(r'^\d+\.?\s*', '', line).strip()
            
            tasks.append({
                'title': clean_line,
                'priority': 'medium',
                'notes': '',
                'estimated_time': '',
                'source': 'original input'
            })
        
        removed_count = len(lines) - len(unique_lines)
        processing_notes = f"Basic grooming: {len(tasks)} tasks"
        if removed_count > 0:
            processing_notes += f", removed {removed_count} duplicates"
        
        return GroomingResult(
            success=True,
            groomed_tasks=tasks,
            processing_notes=processing_notes,
            fallback_used=True,
            suggestions=["Consider using AI grooming for better task optimization"]
        )
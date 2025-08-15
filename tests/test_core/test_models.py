"""
Tests for the core models: Task and TaskManager classes.
"""
import pytest
from datetime import datetime
from unittest.mock import patch

from src.core.models import Task, TaskManager


class TestTask:
    """Test cases for the Task class."""
    
    def test_task_creation(self):
        """Test basic task creation."""
        task = Task("Test Task", "Test description", 30)
        
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.estimated_time == 30
        assert task.dependencies == []
        assert task.completed is False
        assert task.start_time is None
        assert task.end_time is None
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.id, int)
    
    def test_task_creation_minimal(self):
        """Test task creation with minimal parameters."""
        task = Task("Minimal Task")
        
        assert task.title == "Minimal Task"
        assert task.description == ""
        assert task.estimated_time == 0
    
    def test_add_dependency(self, sample_task):
        """Test adding dependencies to a task."""
        dependency = Task("Dependency")
        sample_task.add_dependency(dependency)
        
        assert dependency in sample_task.dependencies
        assert len(sample_task.dependencies) == 1
    
    def test_add_duplicate_dependency(self, sample_task):
        """Test that duplicate dependencies are not added."""
        dependency = Task("Dependency")
        sample_task.add_dependency(dependency)
        sample_task.add_dependency(dependency)  # Add same dependency again
        
        assert len(sample_task.dependencies) == 1
    
    def test_remove_dependency(self, sample_task):
        """Test removing dependencies from a task."""
        dependency = Task("Dependency")
        sample_task.add_dependency(dependency)
        sample_task.remove_dependency(dependency)
        
        assert dependency not in sample_task.dependencies
        assert len(sample_task.dependencies) == 0
    
    def test_remove_nonexistent_dependency(self, sample_task):
        """Test removing a dependency that doesn't exist."""
        dependency = Task("Dependency")
        # Should not raise an error
        sample_task.remove_dependency(dependency)
        assert len(sample_task.dependencies) == 0
    
    def test_can_start_no_dependencies(self, sample_task):
        """Test can_start returns True when task has no dependencies."""
        assert sample_task.can_start() is True
    
    def test_can_start_with_completed_dependencies(self, sample_task):
        """Test can_start returns True when all dependencies are completed."""
        dep1 = Task("Dependency 1")
        dep2 = Task("Dependency 2")
        
        dep1.mark_completed()
        dep2.mark_completed()
        
        sample_task.add_dependency(dep1)
        sample_task.add_dependency(dep2)
        
        assert sample_task.can_start() is True
    
    def test_can_start_with_incomplete_dependencies(self, sample_task):
        """Test can_start returns False when dependencies are not completed."""
        dep1 = Task("Dependency 1")
        dep2 = Task("Dependency 2")
        
        dep1.mark_completed()
        # dep2 is not completed
        
        sample_task.add_dependency(dep1)
        sample_task.add_dependency(dep2)
        
        assert sample_task.can_start() is False
    
    @patch('src.core.models.datetime')
    def test_mark_completed(self, mock_datetime, sample_task):
        """Test marking a task as completed."""
        mock_now = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        
        sample_task.mark_completed()
        
        assert sample_task.completed is True
        assert sample_task.end_time == mock_now
    
    @patch('src.core.models.datetime')
    def test_start_task_can_start(self, mock_datetime, sample_task):
        """Test starting a task that can be started."""
        mock_now = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        
        sample_task.start_task()
        
        assert sample_task.start_time == mock_now
    
    def test_start_task_cannot_start(self, sample_task):
        """Test starting a task that cannot be started due to dependencies."""
        dependency = Task("Dependency")
        sample_task.add_dependency(dependency)
        
        sample_task.start_task()
        
        assert sample_task.start_time is None
    
    def test_start_task_already_completed(self, sample_task):
        """Test starting a task that is already completed."""
        sample_task.mark_completed()
        
        sample_task.start_task()
        
        assert sample_task.start_time is None
    
    def test_str_representation(self, sample_task):
        """Test string representation of a task."""
        assert str(sample_task) == "Task: Test Task"


class TestTaskManager:
    """Test cases for the TaskManager class."""
    
    def test_task_manager_creation(self, task_manager):
        """Test TaskManager creation."""
        assert task_manager.tasks == []
        assert task_manager.current_task is None
    
    def test_add_task(self, task_manager, sample_task):
        """Test adding a task to the manager."""
        task_manager.add_task(sample_task)
        
        assert sample_task in task_manager.tasks
        assert len(task_manager.tasks) == 1
    
    def test_remove_task(self, task_manager, sample_task):
        """Test removing a task from the manager."""
        task_manager.add_task(sample_task)
        task_manager.remove_task(sample_task)
        
        assert sample_task not in task_manager.tasks
        assert len(task_manager.tasks) == 0
    
    def test_remove_task_with_dependencies(self, task_manager):
        """Test removing a task that other tasks depend on."""
        task1 = Task("Task 1")
        task2 = Task("Task 2")
        task2.add_dependency(task1)
        
        task_manager.add_task(task1)
        task_manager.add_task(task2)
        
        task_manager.remove_task(task1)
        
        assert task1 not in task_manager.tasks
        assert task1 not in task2.dependencies
    
    def test_remove_nonexistent_task(self, task_manager, sample_task):
        """Test removing a task that doesn't exist in the manager."""
        # Should not raise an error
        task_manager.remove_task(sample_task)
        assert len(task_manager.tasks) == 0
    
    def test_get_ready_tasks(self, populated_task_manager):
        """Test getting tasks that are ready to start."""
        ready_tasks = populated_task_manager.get_ready_tasks()
        
        # Only task1 should be ready initially (no dependencies)
        assert len(ready_tasks) == 1
        assert ready_tasks[0].title == "Task 1"
    
    def test_get_ready_tasks_after_completion(self, populated_task_manager):
        """Test getting ready tasks after completing dependencies."""
        # Complete task1
        task1 = next(task for task in populated_task_manager.tasks if task.title == "Task 1")
        task1.mark_completed()
        
        ready_tasks = populated_task_manager.get_ready_tasks()
        
        # Now task3 should be ready
        assert len(ready_tasks) == 1
        assert ready_tasks[0].title == "Task 3"
    
    def test_get_completed_tasks(self, populated_task_manager):
        """Test getting completed tasks."""
        task1 = next(task for task in populated_task_manager.tasks if task.title == "Task 1")
        task1.mark_completed()
        
        completed_tasks = populated_task_manager.get_completed_tasks()
        
        assert len(completed_tasks) == 1
        assert completed_tasks[0].title == "Task 1"
    
    def test_get_pending_tasks(self, populated_task_manager):
        """Test getting pending (not completed) tasks."""
        task1 = next(task for task in populated_task_manager.tasks if task.title == "Task 1")
        task1.mark_completed()
        
        pending_tasks = populated_task_manager.get_pending_tasks()
        
        assert len(pending_tasks) == 2
        assert all(not task.completed for task in pending_tasks)
    
    def test_start_task_success(self, task_manager, sample_task):
        """Test starting a task successfully."""
        task_manager.add_task(sample_task)
        
        result = task_manager.start_task(sample_task)
        
        assert result is True
        assert task_manager.current_task == sample_task
        assert sample_task.start_time is not None
    
    def test_start_task_failure(self, task_manager):
        """Test starting a task that cannot be started."""
        task1 = Task("Task 1")
        task2 = Task("Task 2")
        task2.add_dependency(task1)  # task1 is not completed
        
        task_manager.add_task(task1)
        task_manager.add_task(task2)
        
        result = task_manager.start_task(task2)
        
        assert result is False
        assert task_manager.current_task is None
    
    def test_complete_current_task(self, task_manager, sample_task):
        """Test completing the current task."""
        task_manager.add_task(sample_task)
        task_manager.start_task(sample_task)
        
        task_manager.complete_current_task()
        
        assert sample_task.completed is True
        assert task_manager.current_task is None
    
    def test_complete_current_task_no_current_task(self, task_manager):
        """Test completing current task when no task is current."""
        # Should not raise an error
        task_manager.complete_current_task()
        assert task_manager.current_task is None
    
    def test_get_timeline_data_empty(self, task_manager):
        """Test getting timeline data with no tasks."""
        timeline_data = task_manager.get_timeline_data()
        
        assert timeline_data['current_task'] is None
        assert timeline_data['ready_tasks'] == []
        assert timeline_data['parallel_tasks'] == []
        assert timeline_data['upcoming_tasks'] == []
    
    def test_get_timeline_data_with_tasks(self, populated_task_manager):
        """Test getting timeline data with tasks."""
        timeline_data = populated_task_manager.get_timeline_data()
        
        assert timeline_data['current_task'] is None
        assert len(timeline_data['ready_tasks']) == 1
        assert timeline_data['ready_tasks'][0].title == "Task 1"
    
    def test_get_timeline_data_multiple_ready_tasks(self, task_manager):
        """Test timeline data with multiple ready tasks."""
        # Create tasks with no dependencies
        for i in range(3):
            task = Task(f"Ready Task {i+1}")
            task_manager.add_task(task)
        
        timeline_data = task_manager.get_timeline_data()
        
        assert len(timeline_data['ready_tasks']) == 3
        assert len(timeline_data['parallel_tasks']) == 2  # Shows up to 2 parallel tasks
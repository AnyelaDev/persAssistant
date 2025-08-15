"""
Tests for timeline generation functionality.
"""
import pytest
from src.core.models import Task, TaskManager


class TestTimelineGeneration:
    """Test cases for timeline generation functionality."""
    
    def test_timeline_data_structure(self, task_manager):
        """Test that timeline data has the correct structure."""
        timeline_data = task_manager.get_timeline_data()
        
        required_keys = ['current_task', 'ready_tasks', 'parallel_tasks', 'upcoming_tasks']
        assert all(key in timeline_data for key in required_keys)
    
    def test_timeline_empty_manager(self, task_manager):
        """Test timeline generation with empty task manager."""
        timeline_data = task_manager.get_timeline_data()
        
        assert timeline_data['current_task'] is None
        assert timeline_data['ready_tasks'] == []
        assert timeline_data['parallel_tasks'] == []
        assert timeline_data['upcoming_tasks'] == []
    
    def test_timeline_single_ready_task(self, task_manager):
        """Test timeline with one ready task."""
        task = Task("Single Task", "Description", 30)
        task_manager.add_task(task)
        
        timeline_data = task_manager.get_timeline_data()
        
        assert timeline_data['current_task'] is None
        assert len(timeline_data['ready_tasks']) == 1
        assert timeline_data['ready_tasks'][0] == task
        assert timeline_data['parallel_tasks'] == []
    
    def test_timeline_multiple_ready_tasks(self, task_manager):
        """Test timeline with multiple ready tasks (parallel tasks)."""
        tasks = []
        for i in range(4):
            task = Task(f"Ready Task {i+1}", f"Description {i+1}", 15)
            task_manager.add_task(task)
            tasks.append(task)
        
        timeline_data = task_manager.get_timeline_data()
        
        assert len(timeline_data['ready_tasks']) == 4
        assert len(timeline_data['parallel_tasks']) == 2  # Shows up to 2 parallel tasks
        assert timeline_data['parallel_tasks'] == tasks[1:3]
    
    def test_timeline_with_current_task(self, task_manager):
        """Test timeline when a task is currently running."""
        task = Task("Current Task", "Running task", 45)
        task_manager.add_task(task)
        task_manager.start_task(task)
        
        timeline_data = task_manager.get_timeline_data()
        
        assert timeline_data['current_task'] == task
        assert task not in timeline_data['ready_tasks']  # Current task not in ready
    
    def test_timeline_with_dependencies(self, task_manager):
        """Test timeline with task dependencies."""
        task1 = Task("Foundation Task", "Must be done first", 20)
        task2 = Task("Dependent Task", "Depends on foundation", 30)
        task3 = Task("Final Task", "Depends on dependent", 15)
        
        task2.add_dependency(task1)
        task3.add_dependency(task2)
        
        task_manager.add_task(task1)
        task_manager.add_task(task2)
        task_manager.add_task(task3)
        
        timeline_data = task_manager.get_timeline_data()
        
        # Only task1 should be ready initially
        assert len(timeline_data['ready_tasks']) == 1
        assert timeline_data['ready_tasks'][0] == task1
    
    def test_timeline_progression(self, task_manager):
        """Test timeline changes as tasks are completed."""
        task1 = Task("First Task", "Start here", 20)
        task2 = Task("Second Task", "After first", 30)
        task3 = Task("Third Task", "After second", 25)
        
        task2.add_dependency(task1)
        task3.add_dependency(task2)
        
        task_manager.add_task(task1)
        task_manager.add_task(task2)
        task_manager.add_task(task3)
        
        # Initially, only task1 is ready
        timeline_data = task_manager.get_timeline_data()
        assert len(timeline_data['ready_tasks']) == 1
        assert timeline_data['ready_tasks'][0] == task1
        
        # Complete task1
        task1.mark_completed()
        timeline_data = task_manager.get_timeline_data()
        assert len(timeline_data['ready_tasks']) == 1
        assert timeline_data['ready_tasks'][0] == task2
        
        # Complete task2
        task2.mark_completed()
        timeline_data = task_manager.get_timeline_data()
        assert len(timeline_data['ready_tasks']) == 1
        assert timeline_data['ready_tasks'][0] == task3
    
    def test_timeline_parallel_tasks_limit(self, task_manager):
        """Test that parallel tasks are limited to 2."""
        # Add 5 ready tasks
        for i in range(5):
            task = Task(f"Ready Task {i+1}")
            task_manager.add_task(task)
        
        timeline_data = task_manager.get_timeline_data()
        
        assert len(timeline_data['ready_tasks']) == 5
        assert len(timeline_data['parallel_tasks']) == 2  # Limited to 2
    
    def test_timeline_completed_tasks_excluded(self, task_manager):
        """Test that completed tasks are excluded from timeline."""
        task1 = Task("Completed Task")
        task2 = Task("Ready Task")
        
        task1.mark_completed()
        
        task_manager.add_task(task1)
        task_manager.add_task(task2)
        
        timeline_data = task_manager.get_timeline_data()
        
        assert len(timeline_data['ready_tasks']) == 1
        assert timeline_data['ready_tasks'][0] == task2
        assert task1 not in timeline_data['ready_tasks']
    
    def test_timeline_complex_dependency_chain(self, task_manager):
        """Test timeline with complex dependency relationships."""
        # Create a diamond dependency pattern:
        # task1 -> task2, task3 -> task4
        task1 = Task("Base Task")
        task2 = Task("Branch A")
        task3 = Task("Branch B")  
        task4 = Task("Merge Task")
        
        task2.add_dependency(task1)
        task3.add_dependency(task1)
        task4.add_dependency(task2)
        task4.add_dependency(task3)
        
        for task in [task1, task2, task3, task4]:
            task_manager.add_task(task)
        
        # Initially only task1 is ready
        timeline_data = task_manager.get_timeline_data()
        assert len(timeline_data['ready_tasks']) == 1
        assert timeline_data['ready_tasks'][0] == task1
        
        # Complete task1, now task2 and task3 are ready
        task1.mark_completed()
        timeline_data = task_manager.get_timeline_data()
        assert len(timeline_data['ready_tasks']) == 2
        assert task2 in timeline_data['ready_tasks']
        assert task3 in timeline_data['ready_tasks']
        
        # Complete both task2 and task3, now task4 is ready
        task2.mark_completed()
        task3.mark_completed()
        timeline_data = task_manager.get_timeline_data()
        assert len(timeline_data['ready_tasks']) == 1
        assert timeline_data['ready_tasks'][0] == task4
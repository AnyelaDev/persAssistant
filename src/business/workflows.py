"""
Business workflow logic - manages todo workflows without UI dependencies.
"""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from src.core.models import Task, TaskManager


@dataclass
class TimelineData:
    """Data structure for timeline information."""
    ready_tasks: List[Task]
    blocked_tasks: List[Task]
    completed_tasks: List[Task]
    current_task: Optional[Task]


class TodoWorkflow:
    """Manages todo workflow business logic."""
    
    def __init__(self):
        self.task_manager = TaskManager()
        self._task_id_counter = 1
        self._task_id_map: Dict[int, Task] = {}
        
    def add_task(self, title: str, description: str = "", estimated_time: int = 0) -> int:
        """Add a task and return its ID."""
        task = Task(title, description, estimated_time)
        self.task_manager.add_task(task)
        
        # Create a simple ID mapping
        task_id = self._task_id_counter
        self._task_id_map[task_id] = task
        self._task_id_counter += 1
        
        return task_id
        
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self._task_id_map.get(task_id)
        
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self.task_manager.tasks.copy()
        
    def set_dependency(self, task_id: int, depends_on: int) -> bool:
        """Set task dependency. Returns True if successful."""
        task = self._task_id_map.get(task_id)
        dependency = self._task_id_map.get(depends_on)
        
        if task and dependency:
            task.add_dependency(dependency)
            return True
        return False
        
    def start_task(self, task_id: int) -> bool:
        """Start a task. Returns True if successful."""
        task = self._task_id_map.get(task_id)
        if task:
            return self.task_manager.start_task(task)
        return False
        
    def complete_task(self, task_id: int) -> bool:
        """Complete a specific task. Returns True if successful."""
        task = self._task_id_map.get(task_id)
        if task:
            task.mark_completed()
            return True
        return False
        
    def complete_current_task(self) -> bool:
        """Complete the currently running task."""
        if self.task_manager.current_task:
            self.task_manager.complete_current_task()
            return True
        return False
        
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        return self.task_manager.get_completed_tasks()
        
    def generate_timeline(self) -> TimelineData:
        """Generate timeline data for visualization."""
        ready_tasks = self.task_manager.get_ready_tasks()
        all_tasks = self.task_manager.tasks
        completed_tasks = self.task_manager.get_completed_tasks()
        
        # Find blocked tasks (not ready and not completed)
        blocked_tasks = [
            task for task in all_tasks 
            if not task.can_start() and not task.completed
        ]
        
        return TimelineData(
            ready_tasks=ready_tasks,
            blocked_tasks=blocked_tasks,
            completed_tasks=completed_tasks,
            current_task=self.task_manager.current_task
        )
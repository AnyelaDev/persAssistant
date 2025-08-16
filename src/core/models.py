from datetime import datetime, timedelta
from typing import List, Optional


class Task:
    def __init__(self, title: str, description: str = "", estimated_time: int = 0):
        self.id = id(self)  # Simple ID generation
        self.title = title
        self.description = description
        self.estimated_time = estimated_time  # in minutes
        self.dependencies: List['Task'] = []
        self.created_at = datetime.now()
        self.completed = False
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def add_dependency(self, task: 'Task'):
        if task not in self.dependencies:
            self.dependencies.append(task)
    
    def remove_dependency(self, task: 'Task'):
        if task in self.dependencies:
            self.dependencies.remove(task)
    
    def can_start(self) -> bool:
        return all(dep.completed for dep in self.dependencies)
    
    def mark_completed(self):
        self.completed = True
        self.end_time = datetime.now()
    
    def start_task(self):
        if self.can_start() and not self.completed:
            self.start_time = datetime.now()
    
    def __str__(self):
        return f"Task: {self.title}"


class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.current_task: Optional[Task] = None
    
    def add_task(self, task: Task):
        self.tasks.append(task)
    
    def remove_task(self, task: Task):
        if task in self.tasks:
            self.tasks.remove(task)
            # Remove this task from other tasks' dependencies
            for t in self.tasks:
                t.remove_dependency(task)
    
    def get_ready_tasks(self) -> List[Task]:
        return [task for task in self.tasks 
                if task.can_start() and not task.completed and task != self.current_task]
    
    def get_completed_tasks(self) -> List[Task]:
        return [task for task in self.tasks if task.completed]
    
    def get_pending_tasks(self) -> List[Task]:
        return [task for task in self.tasks if not task.completed]
    
    def start_task(self, task: Task):
        if task.can_start():
            self.current_task = task
            task.start_task()
            return True
        return False
    
    def complete_current_task(self):
        if self.current_task:
            self.current_task.mark_completed()
            self.current_task = None
    
    def get_timeline_data(self):
        """Generate timeline data for visualization"""
        timeline_data = {
            'current_task': self.current_task,
            'ready_tasks': self.get_ready_tasks(),
            'parallel_tasks': [],  # Tasks that can be done in parallel
            'upcoming_tasks': []
        }
        
        ready_tasks = self.get_ready_tasks()
        if len(ready_tasks) > 1:
            timeline_data['parallel_tasks'] = ready_tasks[1:3]  # Show up to 2 parallel tasks
        
        return timeline_data


# Global task manager instance
task_manager = TaskManager()
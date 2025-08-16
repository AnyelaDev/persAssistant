"""
Pytest configuration and fixtures for the Personal Assistant app tests.
"""
import pytest
import sys
import os

# Add project root to path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.models import Task, TaskManager

# Import all fixtures from fixtures module
from tests.fixtures.app_fixtures import *
from tests.helpers.test_helpers import *


@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return Task(
        title="Test Task",
        description="A task for testing",
        estimated_time=30
    )


@pytest.fixture
def sample_tasks():
    """Create a list of sample tasks for testing."""
    task1 = Task("Task 1", "First task", 15)
    task2 = Task("Task 2", "Second task", 25)
    task3 = Task("Task 3", "Third task", 10)
    
    # Set up dependencies: task3 depends on task1, task2 depends on both
    task3.add_dependency(task1)
    task2.add_dependency(task1)
    task2.add_dependency(task3)
    
    return [task1, task2, task3]


@pytest.fixture
def task_manager():
    """Create a fresh TaskManager instance for testing."""
    return TaskManager()


@pytest.fixture
def populated_task_manager(sample_tasks):
    """Create a TaskManager with sample tasks."""
    manager = TaskManager()
    for task in sample_tasks:
        manager.add_task(task)
    return manager
"""
Test fixtures for creating real app instances and components for testing.
"""
import pytest
from unittest.mock import Mock, patch
from src.core.app import PersonalAssistantApp, AppScreenManager
from src.core.models import Task, TaskManager


@pytest.fixture
def task_manager():
    """Create a clean TaskManager instance for testing."""
    return TaskManager()


@pytest.fixture
def sample_tasks():
    """Create sample tasks for testing."""
    tasks = [
        Task("Write tests", description="Create comprehensive test suite", estimated_time=120),
        Task("Review code", description="Code review session", estimated_time=60),
        Task("Deploy app", description="Deploy to production", estimated_time=30)
    ]
    
    # Add dependencies
    tasks[1].add_dependency(tasks[0])  # Review depends on Write
    tasks[2].add_dependency(tasks[1])  # Deploy depends on Review
    
    return tasks


@pytest.fixture
def populated_task_manager(task_manager, sample_tasks):
    """Create TaskManager with sample tasks."""
    for task in sample_tasks:
        task_manager.add_task(task)
    return task_manager


@pytest.fixture
def mock_kivy_modules():
    """Mock Kivy modules for testing without GUI."""
    kivy_modules = [
        'kivy',
        'kivy.app',
        'kivy.uix',
        'kivy.uix.screenmanager',
        'kivy.uix.boxlayout',
        'kivy.uix.button',
        'kivy.uix.label',
        'kivy.uix.textinput',
        'kivy.uix.scrollview',
        'kivy.uix.gridlayout',
        'kivy.graphics'
    ]
    
    import sys
    original_modules = {}
    
    # Store original modules and mock them
    for module in kivy_modules:
        if module in sys.modules:
            original_modules[module] = sys.modules[module]
        sys.modules[module] = Mock()
    
    yield
    
    # Restore original modules
    for module, original in original_modules.items():
        sys.modules[module] = original


@pytest.fixture
def test_app_manager(mock_kivy_modules):
    """Create a real AppScreenManager for integration testing."""
    with patch('kivy.uix.screenmanager.ScreenManager.__init__', return_value=None):
        manager = AppScreenManager()
        manager.add_widget = Mock()
        manager.current = 'main_menu'
        manager.screens = {}
        
        # Add mock screens for testing navigation
        expected_screens = [
            'main_menu', 'executive_function', 'todo_timeline',
            'todo_list', 'times_dependencies', 'timeline_view',
            'emotions_management', 'habits', 'pomodoro', 'routines'
        ]
        
        for screen_name in expected_screens:
            mock_screen = Mock()
            mock_screen.name = screen_name
            manager.screens[screen_name] = mock_screen
            
    return manager


@pytest.fixture
def test_app(mock_kivy_modules):
    """Create a real PersonalAssistantApp for E2E testing."""
    with patch('src.core.app.AppScreenManager') as mock_manager_class:
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        
        app = PersonalAssistantApp()
        app.screen_manager = mock_manager
        
        return app
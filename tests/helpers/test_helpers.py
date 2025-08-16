"""
Helper functions for testing user interactions and behaviors.
"""
from unittest.mock import Mock


def simulate_button_press(button_mock, callback_args=None):
    """Simulate a button press event."""
    if hasattr(button_mock, 'bind') and button_mock.bind.called:
        # Get the callback from the bind call
        bind_calls = button_mock.bind.call_args_list
        for call in bind_calls:
            if 'on_press' in call[1]:
                callback = call[1]['on_press']
                if callback_args:
                    callback(*callback_args)
                else:
                    callback(button_mock)
                return True
    return False


def create_mock_screen(screen_name, manager=None):
    """Create a mock screen with basic properties."""
    screen = Mock()
    screen.name = screen_name
    screen.manager = manager
    return screen


def assert_screen_transition(manager, from_screen, to_screen):
    """Assert that screen transition occurred correctly."""
    assert manager.current == to_screen, f"Expected screen '{to_screen}', got '{manager.current}'"


def create_navigation_path(manager, screen_names):
    """Simulate navigation through a series of screens."""
    for screen_name in screen_names:
        manager.switch_to_screen(screen_name)
        assert manager.current == screen_name


class UserActionSimulator:
    """Simulates user actions for behavior testing."""
    
    def __init__(self, app_manager):
        self.manager = app_manager
        
    def navigate_to(self, screen_name):
        """Simulate user navigation to a screen."""
        self.manager.switch_to_screen(screen_name)
        return self.manager.current == screen_name
        
    def go_back(self):
        """Simulate back button press."""
        # This would implement back navigation logic
        pass
        
    def create_task(self, task_data):
        """Simulate user creating a new task."""
        # This would simulate the full task creation flow
        pass


class TestScenarioBuilder:
    """Builder for creating test scenarios."""
    
    def __init__(self):
        self.tasks = []
        self.navigation_flow = []
        
    def with_task(self, name, description="", estimated_time=60):
        """Add a task to the scenario."""
        self.tasks.append({
            'name': name,
            'description': description,
            'estimated_time': estimated_time
        })
        return self
        
    def with_navigation(self, screen_name):
        """Add navigation step to scenario."""
        self.navigation_flow.append(screen_name)
        return self
        
    def build(self):
        """Return the built scenario."""
        return {
            'tasks': self.tasks,
            'navigation_flow': self.navigation_flow
        }


# User Story Test Helpers
def test_user_story(story_description):
    """Decorator for user story tests."""
    def decorator(test_func):
        test_func.user_story = story_description
        return test_func
    return decorator


def given_user_has_tasks(task_manager, task_count=3):
    """Test setup: user has existing tasks."""
    tasks = []
    for i in range(task_count):
        task = Task(f"Task {i+1}", f"Description {i+1}", estimated_time=30)
        task_manager.add_task(task)
        tasks.append(task)
    return tasks


def when_user_navigates_to(manager, screen_name):
    """Test action: user navigates to screen."""
    manager.switch_to_screen(screen_name)
    return manager.current


def then_user_sees_screen(manager, expected_screen):
    """Test assertion: user sees expected screen."""
    assert manager.current == expected_screen, f"User should see {expected_screen}, but sees {manager.current}"
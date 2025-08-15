"""
Business Logic Integration Tests - TDD Style
These tests specify the behavior we want, driving the design of better architecture.
Many of these tests WILL FAIL initially - that's the point!
"""
import pytest
from src.core.models import Task, TaskManager


class TestNavigationLogic:
    """Test navigation business logic separate from UI implementation."""
    
    def test_screen_navigator_tracks_current_screen(self):
        """Test navigation state management."""
        from src.business.navigation import ScreenNavigator  # Will fail - doesn't exist yet!
        
        navigator = ScreenNavigator()
        assert navigator.current_screen == 'main_menu'  # Default
        
        navigator.navigate_to('executive_function')
        assert navigator.current_screen == 'executive_function'
        
    def test_navigation_validates_valid_screens(self):
        """Test that navigation only allows valid screen transitions."""
        from src.business.navigation import ScreenNavigator
        
        navigator = ScreenNavigator()
        
        # Valid navigation should work
        result = navigator.navigate_to('executive_function')
        assert result is True
        assert navigator.current_screen == 'executive_function'
        
        # Invalid navigation should fail gracefully
        result = navigator.navigate_to('non_existent_screen')
        assert result is False
        assert navigator.current_screen == 'executive_function'  # Unchanged
        
    def test_navigation_back_stack(self):
        """Test navigation maintains history for back button."""
        from src.business.navigation import ScreenNavigator
        
        navigator = ScreenNavigator()
        navigator.navigate_to('executive_function')
        navigator.navigate_to('todo_timeline')
        navigator.navigate_to('todo_list')
        
        # Back navigation should work
        navigator.go_back()
        assert navigator.current_screen == 'todo_timeline'
        
        navigator.go_back()
        assert navigator.current_screen == 'executive_function'


class TestTodoWorkflowLogic:
    """Test todo workflow business logic separate from UI."""
    
    def test_todo_workflow_manages_task_creation(self):
        """Test workflow can create and manage tasks."""
        from src.business.workflows import TodoWorkflow  # Will fail - doesn't exist yet!
        
        workflow = TodoWorkflow()
        
        # Add tasks through workflow
        task1_id = workflow.add_task("Write tests", "Create comprehensive tests", 60)
        task2_id = workflow.add_task("Review code", "Code review session", 30)
        
        # Verify tasks were created
        tasks = workflow.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].title == "Write tests"
        assert tasks[1].title == "Review code"
        
    def test_todo_workflow_manages_dependencies(self):
        """Test workflow can set task dependencies."""
        from src.business.workflows import TodoWorkflow
        
        workflow = TodoWorkflow()
        task1_id = workflow.add_task("Foundation", "Base task", 30)
        task2_id = workflow.add_task("Dependent", "Depends on foundation", 20)
        
        # Set dependency
        workflow.set_dependency(task2_id, depends_on=task1_id)
        
        # Verify dependency was set
        task2 = workflow.get_task(task2_id)
        assert not task2.can_start()  # Can't start because dependency not complete
        
        # Complete foundation task
        workflow.complete_task(task1_id)
        
        # Now dependent task can start
        assert task2.can_start()
        
    def test_todo_workflow_generates_timeline(self):
        """Test workflow generates timeline data correctly."""
        from src.business.workflows import TodoWorkflow
        
        workflow = TodoWorkflow()
        task1_id = workflow.add_task("Ready Task 1", "Can start now", 30)
        task2_id = workflow.add_task("Ready Task 2", "Can also start", 20)
        task3_id = workflow.add_task("Blocked Task", "Depends on task 1", 15)
        
        workflow.set_dependency(task3_id, depends_on=task1_id)
        
        # Generate timeline
        timeline = workflow.generate_timeline()
        
        # Verify timeline structure
        assert len(timeline.ready_tasks) == 2  # Tasks 1 and 2
        assert len(timeline.blocked_tasks) == 1  # Task 3
        assert timeline.current_task is None
        
        # Start a task
        workflow.start_task(task1_id)
        timeline = workflow.generate_timeline()
        
        assert timeline.current_task.title == "Ready Task 1"
        assert len(timeline.ready_tasks) == 1  # Only task 2 now


class TestScreenConfiguration:
    """Test that screens expose their configuration for testing."""
    
    def test_main_menu_screen_exposes_navigation_options(self):
        """Test main menu screen provides navigation metadata."""
        from src.ui.screens import MainMenuScreen
        
        screen = MainMenuScreen()
        
        # Screen should expose its navigation options for testing
        options = screen.get_navigation_options()  # Will fail - method doesn't exist!
        
        expected_options = [
            'executive_function',
            'emotions_management', 
            'habits',
            'pomodoro',
            'routines'
        ]
        
        assert set(options) == set(expected_options)
        
    def test_executive_function_screen_exposes_sub_options(self):
        """Test executive function screen provides sub-navigation metadata."""
        from src.ui.screens import ExecutiveFunctionScreen
        
        screen = ExecutiveFunctionScreen()
        
        sub_options = screen.get_navigation_options()  # Will fail - method doesn't exist!
        
        expected_sub_options = [
            'todo_timeline',
            # Add other executive function sub-modules as they're implemented
        ]
        
        assert 'todo_timeline' in sub_options
        
    def test_screen_metadata_consistency(self):
        """Test that all screens have consistent metadata."""
        from src.ui.screens import MainMenuScreen, ExecutiveFunctionScreen, ToDoTimelineScreen
        
        screens = [
            MainMenuScreen(),
            ExecutiveFunctionScreen(), 
            ToDoTimelineScreen()
        ]
        
        for screen in screens:
            # All screens should have basic metadata
            assert hasattr(screen, 'name')
            assert screen.name is not None
            assert isinstance(screen.name, str)
            
            # All screens should expose navigation options
            assert hasattr(screen, 'get_navigation_options')  # Will fail!


class TestUserWorkflowIntegration:
    """Test complete user workflows using business logic."""
    
    def test_complete_todo_creation_workflow(self):
        """Test user can complete full todo creation workflow."""
        from src.business.navigation import ScreenNavigator
        from src.business.workflows import TodoWorkflow
        
        # User starts navigation
        navigator = ScreenNavigator()
        workflow = TodoWorkflow()
        
        # User navigates to todo creation
        navigator.navigate_to('executive_function')
        navigator.navigate_to('todo_timeline') 
        navigator.navigate_to('todo_list')
        
        assert navigator.current_screen == 'todo_list'
        
        # User creates tasks
        task1_id = workflow.add_task("Task 1", "First task", 30)
        task2_id = workflow.add_task("Task 2", "Second task", 45)
        
        # User sets dependencies
        navigator.navigate_to('times_dependencies')
        workflow.set_dependency(task2_id, depends_on=task1_id)
        
        # User views timeline
        navigator.navigate_to('timeline_view')
        timeline = workflow.generate_timeline()
        
        assert len(timeline.ready_tasks) == 1  # Only task 1 ready
        assert timeline.ready_tasks[0].title == "Task 1"
        
    def test_user_can_manage_running_task(self):
        """Test user can start and complete tasks through workflow."""
        from src.business.workflows import TodoWorkflow
        
        workflow = TodoWorkflow()
        task_id = workflow.add_task("Important Task", "Must be done", 60)
        
        # User starts task
        result = workflow.start_task(task_id)
        assert result is True
        
        timeline = workflow.generate_timeline()
        assert timeline.current_task.title == "Important Task"
        
        # User completes task
        workflow.complete_current_task()
        
        timeline = workflow.generate_timeline()
        assert timeline.current_task is None
        
        completed_tasks = workflow.get_completed_tasks()
        assert len(completed_tasks) == 1
        assert completed_tasks[0].title == "Important Task"
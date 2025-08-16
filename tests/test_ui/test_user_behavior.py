"""
Behavior-Focused UI Tests
These tests validate user interactions and outcomes without complex mocking.
They test WHAT users can do, not HOW the UI is implemented.
"""
import pytest
from src.business.navigation import ScreenNavigator
from src.business.workflows import TodoWorkflow
from src.ui.screens import MainMenuScreen, ExecutiveFunctionScreen, ToDoTimelineScreen
from src.core.app import PersonalAssistantApp


class TestUserCanNavigate:
    """Test user navigation behaviors using business logic."""
    
    def test_user_can_navigate_between_main_screens(self):
        """Test user can navigate between all main application screens."""
        navigator = ScreenNavigator()
        
        main_screens = [
            'executive_function',
            'emotions_management',
            'habits', 
            'pomodoro',
            'routines'
        ]
        
        # User can reach each main screen from main menu
        for screen in main_screens:
            navigator.navigate_to('main_menu')
            success = navigator.navigate_to(screen)
            
            assert success is True, f"User should be able to navigate to {screen}"
            assert navigator.current_screen == screen
            
    def test_user_can_complete_todo_workflow_navigation(self):
        """Test user can navigate through complete todo workflow."""
        navigator = ScreenNavigator()
        
        # User wants to create todos and view timeline
        workflow_path = [
            'main_menu',
            'executive_function', 
            'todo_timeline',
            'todo_list',
            'times_dependencies',
            'timeline_view'
        ]
        
        # User should be able to follow this path
        for screen in workflow_path:
            success = navigator.navigate_to(screen)
            assert success is True, f"User should reach {screen} in workflow"
            assert navigator.current_screen == screen
            
    def test_user_can_use_back_navigation(self):
        """Test user can navigate back through screens."""
        navigator = ScreenNavigator()
        
        # User navigates deep into the app
        navigator.navigate_to('executive_function')
        navigator.navigate_to('todo_timeline')
        navigator.navigate_to('todo_list')
        
        # User can navigate back
        navigator.go_back()
        assert navigator.current_screen == 'todo_timeline'
        
        navigator.go_back()
        assert navigator.current_screen == 'executive_function'
        
    def test_user_cannot_navigate_to_invalid_screens(self):
        """Test app gracefully handles invalid navigation."""
        navigator = ScreenNavigator()
        
        invalid_screens = [
            'non_existent_screen',
            'invalid_page',
            '',
            'main_menu_typo'
        ]
        
        original_screen = navigator.current_screen
        
        for invalid_screen in invalid_screens:
            success = navigator.navigate_to(invalid_screen)
            assert success is False, f"Navigation to {invalid_screen} should fail"
            assert navigator.current_screen == original_screen, "Screen should not change on invalid navigation"


class TestUserCanManageTodos:
    """Test user todo management behaviors using business logic."""
    
    def test_user_can_create_and_organize_todos(self):
        """Test user can create todos and organize them."""
        workflow = TodoWorkflow()
        
        # User creates several todos
        task1 = workflow.add_task("Plan project", "Define project scope and timeline", 120)
        task2 = workflow.add_task("Research tools", "Find the right tools for the job", 90)
        task3 = workflow.add_task("Start coding", "Begin implementation", 240)
        
        # User should have created 3 tasks
        all_tasks = workflow.get_all_tasks()
        assert len(all_tasks) == 3
        
        # Tasks should have correct content
        titles = [task.title for task in all_tasks]
        assert "Plan project" in titles
        assert "Research tools" in titles
        assert "Start coding" in titles
        
    def test_user_can_set_task_dependencies(self):
        """Test user can create task dependency relationships."""
        workflow = TodoWorkflow()
        
        # User creates tasks with logical dependencies
        foundation_id = workflow.add_task("Foundation Task", "Must be done first", 60)
        dependent_id = workflow.add_task("Dependent Task", "Requires foundation", 30)
        
        # User sets dependency
        workflow.set_dependency(dependent_id, depends_on=foundation_id)
        
        # Dependent task should not be ready to start
        dependent_task = workflow.get_task(dependent_id)
        assert not dependent_task.can_start(), "Dependent task should not be ready"
        
        # After completing foundation, dependent becomes ready
        workflow.complete_task(foundation_id)
        assert dependent_task.can_start(), "Dependent task should be ready after foundation completes"
        
    def test_user_can_work_on_current_task(self):
        """Test user can start and complete tasks."""
        workflow = TodoWorkflow()
        
        # User creates a task
        task_id = workflow.add_task("Important Work", "Focus on this task", 90)
        
        # User starts the task
        started = workflow.start_task(task_id)
        assert started is True, "User should be able to start task"
        
        # Task should show as current task
        timeline = workflow.generate_timeline()
        assert timeline.current_task is not None
        assert timeline.current_task.title == "Important Work"
        
        # User completes the task
        workflow.complete_current_task()
        
        # Task should be completed
        timeline = workflow.generate_timeline()
        assert timeline.current_task is None
        assert len(timeline.completed_tasks) == 1
        assert timeline.completed_tasks[0].title == "Important Work"
        
    def test_user_sees_correct_timeline_organization(self):
        """Test user sees properly organized timeline."""
        workflow = TodoWorkflow()
        
        # User creates tasks with mixed states
        ready1_id = workflow.add_task("Ready Task 1", "Can start immediately", 30)
        ready2_id = workflow.add_task("Ready Task 2", "Also ready", 45)
        blocked_id = workflow.add_task("Blocked Task", "Cannot start yet", 60)
        
        # Block one task
        workflow.set_dependency(blocked_id, depends_on=ready1_id)
        
        # User views timeline
        timeline = workflow.generate_timeline()
        
        # User should see correct organization
        assert len(timeline.ready_tasks) == 2, "User should see 2 ready tasks"
        assert len(timeline.blocked_tasks) == 1, "User should see 1 blocked task"
        assert timeline.current_task is None, "No task should be running yet"
        
        # User starts a task
        workflow.start_task(ready1_id)
        timeline = workflow.generate_timeline()
        
        # Timeline should update correctly
        assert timeline.current_task.title == "Ready Task 1"
        assert len(timeline.ready_tasks) == 1, "Should have 1 ready task remaining"


class TestUserInterfaceConfiguration:
    """Test UI provides correct user experience."""
    
    def test_screens_provide_user_navigation_options(self):
        """Test screens tell users what they can do."""
        
        # Main menu should show all main features
        main_menu = MainMenuScreen()
        options = main_menu.get_navigation_options()
        
        expected_main_features = {
            'executive_function',
            'emotions_management',
            'habits',
            'pomodoro', 
            'routines'
        }
        
        assert set(options) == expected_main_features, "Main menu should show all main features"
        
        # Executive function should show sub-features
        exec_screen = ExecutiveFunctionScreen()
        exec_options = exec_screen.get_navigation_options()
        
        assert 'todo_timeline' in exec_options, "Executive function should include todo timeline"
        
        # Todo timeline should show workflow steps
        todo_screen = ToDoTimelineScreen()
        todo_options = todo_screen.get_navigation_options()
        
        workflow_steps = {'todo_list', 'times_dependencies', 'timeline_view'}
        assert workflow_steps.issubset(set(todo_options)), "Todo timeline should show workflow steps"
        
    def test_screens_have_consistent_naming(self):
        """Test screens have consistent, user-friendly names."""
        screens = [
            MainMenuScreen(),
            ExecutiveFunctionScreen(),
            ToDoTimelineScreen()
        ]
        
        for screen in screens:
            assert hasattr(screen, 'name'), f"{type(screen).__name__} should have name attribute"
            assert isinstance(screen.name, str), "Screen name should be string"
            assert screen.name.strip(), "Screen name should not be empty"
            assert '_' in screen.name, "Screen names should use snake_case convention"
            
    def test_app_has_user_friendly_configuration(self):
        """Test app provides good user experience."""
        # Test app title configuration
        app = PersonalAssistantApp()
        
        assert hasattr(app, 'title'), "App should have title"
        assert isinstance(app.title, str), "App title should be string"
        assert app.title.strip(), "App title should not be empty"


class TestCompleteUserScenarios:
    """Test complete user scenarios end-to-end."""
    
    def test_new_user_can_create_first_project(self):
        """Test complete scenario: new user creates their first project."""
        # User opens app and navigates to todo creation
        navigator = ScreenNavigator()
        workflow = TodoWorkflow()
        
        # Step 1: User explores the app
        navigator.navigate_to('executive_function')
        navigator.navigate_to('todo_timeline')
        navigator.navigate_to('todo_list')
        
        assert navigator.current_screen == 'todo_list'
        
        # Step 2: User creates project tasks
        task1 = workflow.add_task("Research requirements", "Understand what needs to be built", 120)
        task2 = workflow.add_task("Create plan", "Plan the implementation approach", 90)
        task3 = workflow.add_task("Start implementation", "Begin building the solution", 300)
        
        # Step 3: User sets up dependencies
        navigator.navigate_to('times_dependencies')
        workflow.set_dependency(task2, depends_on=task1)  # Plan depends on research
        workflow.set_dependency(task3, depends_on=task2)  # Implementation depends on plan
        
        # Step 4: User views the organized timeline
        navigator.navigate_to('timeline_view')
        timeline = workflow.generate_timeline()
        
        # User should see properly organized work
        assert len(timeline.ready_tasks) == 1, "Only first task should be ready"
        assert timeline.ready_tasks[0].title == "Research requirements"
        assert len(timeline.blocked_tasks) == 2, "Two tasks should be blocked"
        
        # Step 5: User starts working
        workflow.start_task(task1)
        timeline = workflow.generate_timeline()
        
        assert timeline.current_task.title == "Research requirements"
        
    def test_experienced_user_manages_complex_project(self):
        """Test scenario: experienced user manages complex multi-task project."""
        navigator = ScreenNavigator()
        workflow = TodoWorkflow()
        
        # User quickly creates complex project structure
        tasks = {
            'setup': workflow.add_task("Project setup", "Initialize environment", 30),
            'design': workflow.add_task("System design", "Design architecture", 120),
            'db': workflow.add_task("Database schema", "Design data model", 90),
            'api': workflow.add_task("API implementation", "Build core API", 240),
            'ui': workflow.add_task("User interface", "Build frontend", 180),
            'test': workflow.add_task("Testing", "Comprehensive testing", 120),
            'deploy': workflow.add_task("Deployment", "Deploy to production", 60)
        }
        
        # User sets up complex dependencies
        workflow.set_dependency(tasks['design'], depends_on=tasks['setup'])
        workflow.set_dependency(tasks['db'], depends_on=tasks['design'])
        workflow.set_dependency(tasks['api'], depends_on=tasks['db'])
        workflow.set_dependency(tasks['ui'], depends_on=tasks['design'])
        workflow.set_dependency(tasks['test'], depends_on=tasks['api'])
        workflow.set_dependency(tasks['test'], depends_on=tasks['ui'])
        workflow.set_dependency(tasks['deploy'], depends_on=tasks['test'])
        
        # User views organized timeline
        timeline = workflow.generate_timeline()
        
        # Only setup should be ready initially
        assert len(timeline.ready_tasks) == 1
        assert timeline.ready_tasks[0].title == "Project setup"
        
        # User completes setup, enabling design
        workflow.start_task(tasks['setup'])
        workflow.complete_current_task()
        
        timeline = workflow.generate_timeline()
        assert len(timeline.ready_tasks) == 1
        assert timeline.ready_tasks[0].title == "System design"
        
        # User completes design, enabling both DB and UI
        workflow.start_task(tasks['design'])
        workflow.complete_current_task()
        
        timeline = workflow.generate_timeline()
        ready_titles = [task.title for task in timeline.ready_tasks]
        assert "Database schema" in ready_titles
        assert "User interface" in ready_titles
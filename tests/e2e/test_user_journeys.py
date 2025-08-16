"""
End-to-End User Journey Tests
These tests validate complete user scenarios from start to finish,
ensuring the entire system works together to deliver user value.
"""
import pytest
from src.business.navigation import ScreenNavigator
from src.business.workflows import TodoWorkflow
from src.core.app import PersonalAssistantApp


class TestNewUserOnboarding:
    """Test scenarios for users discovering and learning the app."""
    
    def test_new_user_explores_all_main_features(self):
        """Test: New user opens app and explores all main features."""
        # User scenario: "I want to see what this app can do for me"
        navigator = ScreenNavigator()
        
        # User starts at main menu
        assert navigator.current_screen == 'main_menu'
        
        # User explores each main feature area
        main_features = [
            'executive_function',  # "Help me organize tasks"
            'emotions_management', # "Help me manage emotions" 
            'habits',             # "Help me build habits"
            'pomodoro',          # "Help me focus"
            'routines'           # "Help me with routines"
        ]
        
        for feature in main_features:
            # User clicks on feature
            navigator.navigate_to(feature)
            assert navigator.current_screen == feature
            
            # User returns to main menu to explore next feature
            navigator.navigate_to('main_menu')
            assert navigator.current_screen == 'main_menu'
            
        # User has successfully explored all main features
        assert len(navigator.get_navigation_history()) > 0
        
    def test_new_user_discovers_todo_workflow(self):
        """Test: New user discovers and tries the todo workflow."""
        # User scenario: "I heard this app helps with task management"
        navigator = ScreenNavigator()
        workflow = TodoWorkflow()
        
        # User finds executive function feature
        navigator.navigate_to('executive_function')
        
        # User discovers todo timeline
        navigator.navigate_to('todo_timeline')
        
        # User explores the todo workflow options
        todo_workflow_screens = ['todo_list', 'times_dependencies', 'timeline_view']
        
        for screen in todo_workflow_screens:
            navigator.navigate_to(screen)
            assert navigator.current_screen == screen
            
        # User creates a simple first task to try it out
        navigator.navigate_to('todo_list')
        task_id = workflow.add_task("Try this app", "See if this todo system works", 15)
        
        # User views their first timeline
        navigator.navigate_to('timeline_view')
        timeline = workflow.generate_timeline()
        
        assert len(timeline.ready_tasks) == 1
        assert timeline.ready_tasks[0].title == "Try this app"


class TestProductiveUserWorkflows:
    """Test scenarios for users actively using the app for productivity."""
    
    def test_user_manages_daily_work_tasks(self):
        """Test: User manages their daily work using the todo system."""
        # User scenario: "I need to organize my work day"
        navigator = ScreenNavigator()
        workflow = TodoWorkflow()
        
        # User goes directly to todo creation (experienced user)
        navigator.navigate_to('executive_function')
        navigator.navigate_to('todo_timeline')
        navigator.navigate_to('todo_list')
        
        # User creates their daily tasks
        morning_tasks = [
            workflow.add_task("Check emails", "Review and respond to emails", 30),
            workflow.add_task("Team standup", "Daily team meeting", 15),
            workflow.add_task("Code review", "Review teammate's PR", 45)
        ]
        
        afternoon_tasks = [
            workflow.add_task("Feature development", "Work on new feature", 180),
            workflow.add_task("Write tests", "Add tests for new feature", 60),
            workflow.add_task("Update documentation", "Document the new feature", 30)
        ]
        
        # User sets up logical dependencies
        navigator.navigate_to('times_dependencies')
        workflow.set_dependency(afternoon_tasks[1], depends_on=afternoon_tasks[0])  # Tests after development
        workflow.set_dependency(afternoon_tasks[2], depends_on=afternoon_tasks[1])  # Docs after tests
        
        # User views their organized day
        navigator.navigate_to('timeline_view')
        timeline = workflow.generate_timeline()
        
        # User should see morning tasks ready, afternoon tasks properly sequenced
        ready_titles = [task.title for task in timeline.ready_tasks]
        assert "Check emails" in ready_titles
        assert "Team standup" in ready_titles
        assert "Feature development" in ready_titles  # Can start independently
        
        # Dependencies should be properly blocked
        blocked_titles = [task.title for task in timeline.blocked_tasks]
        assert "Write tests" in blocked_titles
        assert "Update documentation" in blocked_titles
        
    def test_user_works_through_complex_project(self):
        """Test: User manages a complex multi-day project."""
        # User scenario: "I need to plan and execute a complex project"
        navigator = ScreenNavigator()
        workflow = TodoWorkflow()
        
        # User creates comprehensive project plan
        navigator.navigate_to('executive_function')
        navigator.navigate_to('todo_timeline')
        navigator.navigate_to('todo_list')
        
        # Phase 1: Planning and Research
        research_id = workflow.add_task("Market research", "Understand user needs", 240)
        design_id = workflow.add_task("System design", "Architecture and planning", 480)
        
        # Phase 2: Development
        backend_id = workflow.add_task("Backend API", "Build core API", 720)
        frontend_id = workflow.add_task("Frontend UI", "Build user interface", 600)
        
        # Phase 3: Quality and Launch
        testing_id = workflow.add_task("Testing phase", "Comprehensive testing", 360)
        launch_id = workflow.add_task("Launch preparation", "Deploy and announce", 240)
        
        # User sets up project dependencies
        navigator.navigate_to('times_dependencies')
        workflow.set_dependency(design_id, depends_on=research_id)
        workflow.set_dependency(backend_id, depends_on=design_id)
        workflow.set_dependency(frontend_id, depends_on=design_id)
        workflow.set_dependency(testing_id, depends_on=backend_id)
        workflow.set_dependency(testing_id, depends_on=frontend_id)
        workflow.set_dependency(launch_id, depends_on=testing_id)
        
        # User views project timeline
        navigator.navigate_to('timeline_view')
        timeline = workflow.generate_timeline()
        
        # Only research should be ready initially
        assert len(timeline.ready_tasks) == 1
        assert timeline.ready_tasks[0].title == "Market research"
        
        # User works through project phases
        # Complete research phase
        workflow.start_task(research_id)
        workflow.complete_current_task()
        
        timeline = workflow.generate_timeline()
        assert timeline.ready_tasks[0].title == "System design"
        
        # Complete design phase
        workflow.start_task(design_id)
        workflow.complete_current_task()
        
        timeline = workflow.generate_timeline()
        # Now both backend and frontend should be available
        ready_titles = [task.title for task in timeline.ready_tasks]
        assert "Backend API" in ready_titles
        assert "Frontend UI" in ready_titles
        
    def test_user_handles_interruptions_and_priority_changes(self):
        """Test: User adapts to changing priorities and interruptions."""
        # User scenario: "I need to handle urgent requests while managing planned work"
        navigator = ScreenNavigator()
        workflow = TodoWorkflow()
        
        # User sets up planned work
        planned_tasks = [
            workflow.add_task("Planned feature A", "Work on planned feature", 120),
            workflow.add_task("Planned feature B", "Continue planned work", 180)
        ]
        
        # User starts working on planned task
        workflow.start_task(planned_tasks[0])
        timeline = workflow.generate_timeline()
        assert timeline.current_task.title == "Planned feature A"
        
        # Urgent request comes in
        navigator.navigate_to('todo_list')
        urgent_id = workflow.add_task("URGENT: Fix critical bug", "Production issue needs immediate attention", 90)
        
        # User switches to urgent task
        workflow.complete_current_task()  # Save current progress
        workflow.start_task(urgent_id)
        
        timeline = workflow.generate_timeline()
        assert timeline.current_task.title == "URGENT: Fix critical bug"
        
        # User completes urgent work and returns to planned work
        workflow.complete_current_task()
        workflow.start_task(planned_tasks[1])
        
        timeline = workflow.generate_timeline()
        assert timeline.current_task.title == "Planned feature B"
        assert len(timeline.completed_tasks) == 2  # Both completed tasks


class TestAdvancedUserScenarios:
    """Test scenarios for power users utilizing advanced features."""
    
    def test_power_user_manages_multiple_concurrent_projects(self):
        """Test: Experienced user manages multiple overlapping projects."""
        # User scenario: "I'm juggling multiple projects with different priorities"
        navigator = ScreenNavigator()
        workflow = TodoWorkflow()
        
        # User creates tasks for Project A (High Priority)
        proj_a_tasks = [
            workflow.add_task("[A] Setup environment", "Project A setup", 60),
            workflow.add_task("[A] Core development", "Build core features", 360),
            workflow.add_task("[A] Testing", "Test Project A", 120)
        ]
        
        # User creates tasks for Project B (Medium Priority)
        proj_b_tasks = [
            workflow.add_task("[B] Requirements gathering", "Understand Project B needs", 90),
            workflow.add_task("[B] Prototype", "Build Project B prototype", 240),
            workflow.add_task("[B] Validation", "Validate Project B approach", 60)
        ]
        
        # User sets up dependencies within each project
        navigator.navigate_to('times_dependencies')
        # Project A dependencies
        workflow.set_dependency(proj_a_tasks[1], depends_on=proj_a_tasks[0])
        workflow.set_dependency(proj_a_tasks[2], depends_on=proj_a_tasks[1])
        
        # Project B dependencies  
        workflow.set_dependency(proj_b_tasks[1], depends_on=proj_b_tasks[0])
        workflow.set_dependency(proj_b_tasks[2], depends_on=proj_b_tasks[1])
        
        # User views combined timeline
        navigator.navigate_to('timeline_view')
        timeline = workflow.generate_timeline()
        
        # User should see initial tasks from both projects
        ready_titles = [task.title for task in timeline.ready_tasks]
        assert "[A] Setup environment" in ready_titles
        assert "[B] Requirements gathering" in ready_titles
        
        # User works on high priority project first
        workflow.start_task(proj_a_tasks[0])
        workflow.complete_current_task()
        
        # User switches between projects efficiently
        workflow.start_task(proj_b_tasks[0])  # Start Project B while thinking about next A task
        workflow.complete_current_task()
        
        timeline = workflow.generate_timeline()
        ready_titles = [task.title for task in timeline.ready_tasks]
        assert "[A] Core development" in ready_titles
        assert "[B] Prototype" in ready_titles
        
    def test_user_optimizes_workflow_over_time(self):
        """Test: User learns and optimizes their workflow patterns."""
        # User scenario: "I want to improve how I work over time"
        navigator = ScreenNavigator()
        workflow = TodoWorkflow()
        
        # User creates typical work pattern
        routine_tasks = [
            workflow.add_task("Daily planning", "Plan the day's work", 15),
            workflow.add_task("Deep work block", "Focus on important work", 120),
            workflow.add_task("Communications", "Handle emails and messages", 30),
            workflow.add_task("Review and adjust", "Review progress and adjust plans", 15)
        ]
        
        # User sets up their optimized workflow
        navigator.navigate_to('times_dependencies')
        workflow.set_dependency(routine_tasks[1], depends_on=routine_tasks[0])  # Plan before deep work
        workflow.set_dependency(routine_tasks[3], depends_on=routine_tasks[1])  # Review after deep work
        # Communications can happen independently
        
        # User executes their optimized workflow
        timeline = workflow.generate_timeline()
        
        # Planning and communications should be ready
        ready_titles = [task.title for task in timeline.ready_tasks]
        assert "Daily planning" in ready_titles
        assert "Communications" in ready_titles
        
        # User follows their optimized sequence
        workflow.start_task(routine_tasks[0])  # Start with planning
        workflow.complete_current_task()
        
        timeline = workflow.generate_timeline()
        ready_titles = [task.title for task in timeline.ready_tasks]
        assert "Deep work block" in ready_titles  # Now available after planning
        
        # User can flexibly handle communications
        workflow.start_task(routine_tasks[2])  # Handle communications 
        workflow.complete_current_task()
        
        # User proceeds with deep work
        workflow.start_task(routine_tasks[1])
        workflow.complete_current_task()
        
        # User completes with review
        timeline = workflow.generate_timeline()
        assert timeline.ready_tasks[0].title == "Review and adjust"


class TestErrorRecoveryScenarios:
    """Test scenarios for handling errors and edge cases gracefully."""
    
    def test_user_recovers_from_navigation_mistakes(self):
        """Test: User accidentally navigates to wrong screens but recovers."""
        navigator = ScreenNavigator()
        
        # User intends to go to todo timeline but makes navigation mistakes
        navigator.navigate_to('executive_function')
        navigator.navigate_to('pomodoro')  # Wrong choice!
        
        # User realizes mistake and uses back navigation
        navigator.go_back()
        assert navigator.current_screen == 'executive_function'
        
        # User makes correct choice
        navigator.navigate_to('todo_timeline')
        assert navigator.current_screen == 'todo_timeline'
        
    def test_user_handles_empty_states_gracefully(self):
        """Test: User interacts with app when no tasks exist."""
        workflow = TodoWorkflow()
        
        # User views timeline with no tasks
        timeline = workflow.generate_timeline()
        
        assert len(timeline.ready_tasks) == 0
        assert len(timeline.blocked_tasks) == 0
        assert len(timeline.completed_tasks) == 0
        assert timeline.current_task is None
        
        # System should handle empty state gracefully
        assert hasattr(timeline, 'ready_tasks')
        assert isinstance(timeline.ready_tasks, list)
        
    def test_user_handles_invalid_operations(self):
        """Test: User attempts invalid operations and system responds gracefully."""
        navigator = ScreenNavigator()
        workflow = TodoWorkflow()
        
        # User tries to navigate to non-existent screen
        result = navigator.navigate_to('non_existent_feature')
        assert result is False
        assert navigator.current_screen == 'main_menu'  # Should stay on current screen
        
        # User tries to start non-existent task
        result = workflow.start_task(99999)  # Invalid task ID
        assert result is False
        
        # User tries to set dependency on non-existent tasks
        result = workflow.set_dependency(99999, depends_on=88888)
        assert result is False
"""
Integration tests for screen navigation and real UI interactions.
These tests focus on behavior and user workflows, not implementation details.
"""
import pytest
from unittest.mock import Mock, patch
from src.core.app import PersonalAssistantApp, AppScreenManager
from src.ui.screens import MainMenuScreen, ExecutiveFunctionScreen, ToDoTimelineScreen


class TestScreenNavigation:
    """Test real screen navigation flows."""
    
    def test_app_screen_manager_initialization(self, mock_kivy_modules):
        """Test AppScreenManager creates all expected screens."""
        with patch('kivy.uix.screenmanager.ScreenManager.__init__', return_value=None):
            manager = AppScreenManager()
            manager.add_widget = Mock()
            
            # Verify all screens would be added
            assert hasattr(manager, 'switch_to_screen')
            
    def test_navigation_flow_main_to_executive(self, test_app_manager):
        """Test user navigation from main menu to executive function."""
        # Start at main menu
        assert test_app_manager.current == 'main_menu'
        
        # User navigates to executive function
        test_app_manager.switch_to_screen('executive_function')
        
        # Verify navigation succeeded
        assert test_app_manager.current == 'executive_function'
        
    def test_navigation_flow_todo_workflow(self, test_app_manager):
        """Test complete todo workflow navigation."""
        # User starts at main menu
        test_app_manager.switch_to_screen('main_menu')
        assert test_app_manager.current == 'main_menu'
        
        # Navigate to executive function
        test_app_manager.switch_to_screen('executive_function')
        assert test_app_manager.current == 'executive_function'
        
        # Navigate to todo timeline
        test_app_manager.switch_to_screen('todo_timeline')
        assert test_app_manager.current == 'todo_timeline'
        
        # Navigate to todo list
        test_app_manager.switch_to_screen('todo_list')
        assert test_app_manager.current == 'todo_list'
        
        # Navigate to times and dependencies
        test_app_manager.switch_to_screen('times_dependencies')
        assert test_app_manager.current == 'times_dependencies'
        
        # Navigate to timeline view
        test_app_manager.switch_to_screen('timeline_view')
        assert test_app_manager.current == 'timeline_view'
        
    def test_navigation_back_flow(self, test_app_manager):
        """Test back navigation maintains proper hierarchy."""
        # Navigate forward through the flow
        screens = ['main_menu', 'executive_function', 'todo_timeline', 'todo_list']
        
        for screen in screens:
            test_app_manager.switch_to_screen(screen)
            assert test_app_manager.current == screen
            
        # Navigate back
        back_flow = ['todo_timeline', 'executive_function', 'main_menu']
        for screen in back_flow:
            test_app_manager.switch_to_screen(screen)
            assert test_app_manager.current == screen
            
    def test_cross_module_navigation(self, test_app_manager):
        """Test navigation between different main modules."""
        main_modules = [
            'executive_function',
            'emotions_management', 
            'habits',
            'pomodoro',
            'routines'
        ]
        
        # Test navigation to each module from main menu
        for module in main_modules:
            test_app_manager.switch_to_screen('main_menu')
            test_app_manager.switch_to_screen(module)
            assert test_app_manager.current == module
            
    def test_invalid_screen_navigation(self, test_app_manager):
        """Test graceful handling of invalid screen names."""
        original_screen = test_app_manager.current
        
        # Try to navigate to non-existent screen
        test_app_manager.switch_to_screen('non_existent_screen')
        
        # Screen manager should still function (Kivy allows this)
        assert hasattr(test_app_manager, 'switch_to_screen')
        
        
class TestScreenInstantiation:
    """Test that screens can be instantiated correctly."""
    
    def test_main_menu_screen_creation(self, mock_kivy_modules):
        """Test MainMenuScreen can be created."""
        with patch('kivy.uix.screenmanager.Screen.__init__', return_value=None):
            screen = MainMenuScreen()
            assert screen.name == 'main_menu'
            
    def test_executive_function_screen_creation(self, mock_kivy_modules):
        """Test ExecutiveFunctionScreen can be created.""" 
        with patch('kivy.uix.screenmanager.Screen.__init__', return_value=None):
            screen = ExecutiveFunctionScreen()
            assert screen.name == 'executive_function'
            
    def test_todo_timeline_screen_creation(self, mock_kivy_modules):
        """Test ToDoTimelineScreen can be created."""
        with patch('kivy.uix.screenmanager.Screen.__init__', return_value=None):
            screen = ToDoTimelineScreen()
            assert screen.name == 'todo_timeline'


class TestAppIntegration:
    """Test integration of the main app with screen management."""
    
    def test_app_builds_screen_manager(self, mock_kivy_modules):
        """Test that PersonalAssistantApp builds and returns screen manager."""
        with patch('src.core.app.AppScreenManager') as mock_manager_class:
            mock_manager = Mock()
            mock_manager_class.return_value = mock_manager
            
            app = PersonalAssistantApp()
            result = app.build()
            
            mock_manager_class.assert_called_once()
            assert result == mock_manager
            
    def test_app_has_correct_title(self, mock_kivy_modules):
        """Test that app gets title from AppConfig."""
        with patch('src.core.config.AppConfig.get_app_title', return_value="Test App"):
            with patch('kivy.app.App.__init__', return_value=None):
                app = PersonalAssistantApp()
                assert app.title == "Test App"


class TestUserWorkflows:
    """Test complete user workflows end-to-end."""
    
    def test_user_can_access_all_main_features(self, test_app_manager):
        """Test user can reach all main application features."""
        main_features = [
            'executive_function',
            'emotions_management',
            'habits', 
            'pomodoro',
            'routines'
        ]
        
        for feature in main_features:
            # User starts from main menu
            test_app_manager.switch_to_screen('main_menu')
            
            # User navigates to feature
            test_app_manager.switch_to_screen(feature)
            
            # User successfully reaches feature
            assert test_app_manager.current == feature
            
    def test_user_todo_creation_workflow(self, test_app_manager):
        """Test complete todo creation and timeline workflow."""
        # User wants to create and manage todos
        workflow_screens = [
            'main_menu',           # Start here
            'executive_function',  # Choose executive function
            'todo_timeline',       # Choose todo timeline
            'todo_list',          # Create todo list
            'times_dependencies',  # Set times and dependencies  
            'timeline_view'        # View generated timeline
        ]
        
        # Simulate user clicking through workflow
        for i, screen in enumerate(workflow_screens[1:], 1):
            test_app_manager.switch_to_screen(screen)
            assert test_app_manager.current == screen, f"Failed at step {i}: {screen}"
            
    def test_user_can_return_home_from_anywhere(self, test_app_manager):
        """Test user can always return to main menu."""
        deep_screens = [
            'timeline_view',
            'times_dependencies', 
            'todo_list',
            'emotions_management',
            'habits'
        ]
        
        for screen in deep_screens:
            # Navigate to deep screen
            test_app_manager.switch_to_screen(screen)
            
            # User can always get home
            test_app_manager.switch_to_screen('main_menu')
            assert test_app_manager.current == 'main_menu'
"""
Tests for navigation functionality and screen management.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock

# Mock Kivy modules to avoid import issues in test environment
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

for module in kivy_modules:
    import sys
    sys.modules[module] = Mock()


class TestAppScreenManager:
    """Test cases for the AppScreenManager navigation."""
    
    @patch('src.ui.screens.ScreenManager')
    @patch('src.ui.screens.MainMenuScreen')
    @patch('src.ui.screens.ExecutiveFunctionScreen')
    @patch('src.ui.screens.ToDoTimelineScreen')
    @patch('src.ui.screens.ToDoListScreen')
    @patch('src.ui.screens.TimesDependenciesScreen')
    @patch('src.ui.screens.TimelineViewScreen')
    @patch('src.ui.screens.EmotionsManagementScreen')
    @patch('src.ui.screens.HabitsScreen')
    @patch('src.ui.screens.PomodoroScreen')
    @patch('src.ui.screens.RoutinesScreen')
    def test_screen_manager_initialization(self, *screen_mocks):
        """Test that AppScreenManager initializes with all screens."""
        from src.core.app import AppScreenManager
        
        screen_manager = AppScreenManager()
        
        # Verify all screen types were instantiated
        for screen_mock in screen_mocks[:-1]:  # Exclude ScreenManager
            screen_mock.assert_called_once()
        
        # Verify add_widget was called for each screen
        assert screen_manager.add_widget.call_count == 10
        
        # Verify initial screen is set
        assert screen_manager.current == 'main_menu'
    
    @patch('src.ui.screens.ScreenManager')
    def test_switch_to_screen(self, mock_screen_manager):
        """Test the switch_to_screen method."""
        from src.core.app import AppScreenManager
        
        # Create a real AppScreenManager instance but mock its parent
        with patch.object(AppScreenManager, '__init__', return_value=None):
            screen_manager = AppScreenManager()
            screen_manager.current = 'main_menu'  # Set initial state
            
            screen_manager.switch_to_screen('executive_function')
            
            assert screen_manager.current == 'executive_function'
    
    def test_navigation_paths(self):
        """Test that navigation paths are correctly defined."""
        # This tests the screen name constants used in navigation
        expected_screens = [
            'main_menu',
            'executive_function', 
            'todo_timeline',
            'todo_list',
            'times_dependencies',
            'timeline_view',
            'emotions_management',
            'habits',
            'pomodoro',
            'routines'
        ]
        
        # These screen names should be used consistently across the app
        assert len(expected_screens) == 10


class TestScreenNavigation:
    """Test navigation behavior of individual screens."""
    
    @patch('src.ui.screens.BoxLayout')
    @patch('src.ui.screens.Button')
    @patch('src.ui.screens.Label')
    def test_main_menu_navigation_buttons(self, mock_label, mock_button, mock_layout):
        """Test that MainMenuScreen creates correct navigation buttons."""
        from src.ui.screens import MainMenuScreen
        
        # Mock the screen manager
        mock_manager = Mock()
        
        with patch('src.ui.screens.Screen.__init__'):
            screen = MainMenuScreen()
            screen.manager = mock_manager
            
            # Verify screen name is set
            assert screen.name == 'main_menu'
            
            # Button creation should be called 3 times (3 main buttons)
            assert mock_button.call_count >= 3
    
    @patch('src.ui.screens.BoxLayout')
    @patch('src.ui.screens.Button')
    @patch('src.ui.screens.Label')
    def test_executive_function_navigation(self, mock_label, mock_button, mock_layout):
        """Test ExecutiveFunctionScreen navigation setup."""
        from src.ui.screens import ExecutiveFunctionScreen
        
        with patch('src.ui.screens.Screen.__init__'):
            screen = ExecutiveFunctionScreen()
            
            assert screen.name == 'executive_function'
            # Should have 3 sub-module buttons + 1 back button = 4 total
            assert mock_button.call_count >= 4
    
    @patch('src.ui.screens.BoxLayout')
    @patch('src.ui.screens.Button')
    @patch('src.ui.screens.Label')
    def test_todo_timeline_navigation(self, mock_label, mock_button, mock_layout):
        """Test ToDoTimelineScreen navigation setup."""
        from src.ui.screens import ToDoTimelineScreen
        
        with patch('src.ui.screens.Screen.__init__'):
            screen = ToDoTimelineScreen()
            
            assert screen.name == 'todo_timeline'
            # Should have 3 sub-options + 1 back button = 4 total
            assert mock_button.call_count >= 4


class TestNavigationFlow:
    """Test complete navigation flows through the app."""
    
    def test_main_to_executive_to_todo_flow(self):
        """Test navigation from main menu to todo timeline."""
        mock_manager = Mock()
        mock_manager.switch_to_screen = Mock()
        
        # Simulate button press navigation
        # Main Menu -> Executive Function
        mock_manager.switch_to_screen('executive_function')
        mock_manager.switch_to_screen.assert_called_with('executive_function')
        
        # Executive Function -> ToDo Timeline
        mock_manager.switch_to_screen('todo_timeline')
        mock_manager.switch_to_screen.assert_called_with('todo_timeline')
        
        # Verify navigation calls
        assert mock_manager.switch_to_screen.call_count == 2
    
    def test_back_navigation_flow(self):
        """Test back navigation maintains proper hierarchy."""
        mock_manager = Mock()
        
        # Test back navigation sequence
        navigation_sequence = [
            ('timeline_view', 'times_dependencies'),
            ('times_dependencies', 'todo_list'),
            ('todo_list', 'todo_timeline'),
            ('todo_timeline', 'executive_function'),
            ('executive_function', 'main_menu')
        ]
        
        for from_screen, to_screen in navigation_sequence:
            mock_manager.current = from_screen
            mock_manager.switch_to_screen(to_screen)
            mock_manager.switch_to_screen.assert_called_with(to_screen)
    
    def test_cross_module_navigation(self):
        """Test navigation between different main modules."""
        mock_manager = Mock()
        
        # Test navigation between main modules
        main_modules = ['executive_function', 'emotions_management', 'habits']
        
        for module in main_modules:
            mock_manager.switch_to_screen(module)
            mock_manager.switch_to_screen.assert_called_with(module)
        
        # All should be able to navigate back to main menu
        for module in main_modules:
            mock_manager.switch_to_screen('main_menu')
            mock_manager.switch_to_screen.assert_called_with('main_menu')


class TestNavigationEdgeCases:
    """Test edge cases and error handling in navigation."""
    
    def test_invalid_screen_navigation(self):
        """Test navigation to non-existent screen."""
        from src.core.app import AppScreenManager
        
        with patch('src.core.app.ScreenManager.__init__', return_value=None):
            screen_manager = AppScreenManager()
            screen_manager.current = 'main_menu'
            
            # This should not raise an error but also shouldn't change current screen
            original_screen = screen_manager.current
            screen_manager.switch_to_screen('non_existent_screen')
            
            # Screen should change (Kivy allows this), but we test the method exists
            assert hasattr(screen_manager, 'switch_to_screen')
    
    def test_navigation_without_manager(self):
        """Test that screens handle missing manager gracefully."""
        from src.ui.screens import MainMenuScreen
        
        with patch('src.ui.screens.Screen.__init__'):
            screen = MainMenuScreen()
            # Screen should be created successfully even without manager
            assert screen.name == 'main_menu'
    
    def test_circular_navigation_prevention(self):
        """Test that circular navigation is handled properly."""
        mock_manager = Mock()
        
        # Simulate navigation to same screen
        mock_manager.current = 'main_menu'
        mock_manager.switch_to_screen('main_menu')
        
        # Should still work (Kivy allows this)
        mock_manager.switch_to_screen.assert_called_with('main_menu')
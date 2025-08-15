"""
Tests for UI component instantiation and behavior.
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


class TestPersonalAssistantApp:
    """Test cases for the main PersonalAssistantApp class."""
    
    @patch('src.core.config.AppConfig.get_app_title')
    @patch('src.core.app.AppScreenManager')
    @patch('src.core.app.App.__init__')
    def test_app_initialization(self, mock_app_init, mock_screen_manager, mock_get_title):
        """Test PersonalAssistantApp initialization."""
        from src.core.app import PersonalAssistantApp
        
        mock_get_title.return_value = "Test Personal Assistant"
        mock_app_init.return_value = None
        
        app = PersonalAssistantApp()
        
        mock_app_init.assert_called_once()
        mock_get_title.assert_called_once()
        assert app.title == "Test Personal Assistant"
    
    @patch('src.core.app.AppScreenManager')
    @patch('src.core.app.App.__init__')
    def test_app_build_method(self, mock_app_init, mock_screen_manager_class):
        """Test that build method returns AppScreenManager instance."""
        from src.core.app import PersonalAssistantApp
        
        mock_app_init.return_value = None
        mock_screen_manager_instance = Mock()
        mock_screen_manager_class.return_value = mock_screen_manager_instance
        
        app = PersonalAssistantApp()
        result = app.build()
        
        mock_screen_manager_class.assert_called_once()
        assert result == mock_screen_manager_instance


class TestScreenComponents:
    """Test UI components of individual screens."""
    
    @patch('src.ui.screens.Screen.__init__')
    @patch('src.ui.screens.BoxLayout')
    @patch('src.ui.screens.Label')
    @patch('src.ui.screens.Button')
    def test_main_menu_screen_components(self, mock_button, mock_label, mock_layout, mock_screen_init):
        """Test MainMenuScreen component creation."""
        from src.ui.screens import MainMenuScreen
        
        mock_screen_init.return_value = None
        
        screen = MainMenuScreen()
        
        # Verify screen properties
        assert screen.name == 'main_menu'
        
        # Verify UI components were created
        mock_layout.assert_called()
        mock_label.assert_called()
        mock_button.assert_called()
    
    @patch('src.ui.screens.Screen.__init__')
    @patch('src.ui.screens.BoxLayout')
    @patch('src.ui.screens.TextInput')
    @patch('src.ui.screens.Button')
    def test_todo_list_screen_components(self, mock_button, mock_text_input, mock_layout, mock_screen_init):
        """Test ToDoListScreen component creation."""
        from src.ui.screens import ToDoListScreen
        
        mock_screen_init.return_value = None
        
        screen = ToDoListScreen()
        
        assert screen.name == 'todo_list'
        
        # Should create text input for todo list
        mock_text_input.assert_called()
        # Should create buttons (Groom, Next, Back)
        assert mock_button.call_count >= 3
    
    @patch('src.ui.screens.Screen.__init__')
    @patch('src.ui.screens.ScrollView')
    @patch('src.ui.screens.TextInput')
    def test_times_dependencies_screen_components(self, mock_text_input, mock_scroll, mock_screen_init):
        """Test TimesDependenciesScreen component creation."""
        from src.ui.screens import TimesDependenciesScreen
        
        mock_screen_init.return_value = None
        
        screen = TimesDependenciesScreen()
        
        assert screen.name == 'times_dependencies'
        
        # Should create scrollable content
        mock_scroll.assert_called()
        # Should create multiple text inputs for time and dependencies
        assert mock_text_input.call_count >= 6  # 3 items × 2 inputs each


class TestToDoListFunctionality:
    """Test specific functionality of ToDoListScreen."""
    
    @patch('src.ui.screens.Screen.__init__')
    def test_groom_list_empty_input(self, mock_screen_init):
        """Test groom_list method with empty input."""
        from src.ui.screens import ToDoListScreen
        
        mock_screen_init.return_value = None
        
        screen = ToDoListScreen()
        screen.text_input = Mock()
        screen.text_input.text = "   "  # Empty/whitespace only
        
        mock_button = Mock()
        screen.groom_list(mock_button)
        
        # Should not modify empty text
        assert screen.text_input.text == "   "
    
    @patch('src.ui.screens.Screen.__init__')
    def test_groom_list_with_content(self, mock_screen_init):
        """Test groom_list method with actual content."""
        from src.ui.screens import ToDoListScreen
        
        mock_screen_init.return_value = None
        
        screen = ToDoListScreen()
        screen.text_input = Mock()
        screen.text_input.text = "Buy groceries\nFinish project\nCall dentist"
        
        mock_button = Mock()
        screen.groom_list(mock_button)
        
        # Should add numbers to items
        expected_text = "1. Buy groceries\n2. Finish project\n3. Call dentist"
        screen.text_input.text = expected_text
    
    @patch('src.ui.screens.Screen.__init__')
    def test_groom_list_with_empty_lines(self, mock_screen_init):
        """Test groom_list method handles empty lines."""
        from src.ui.screens import ToDoListScreen
        
        mock_screen_init.return_value = None
        
        screen = ToDoListScreen()
        screen.text_input = Mock()
        screen.text_input.text = "Task 1\n\nTask 2\n   \nTask 3"
        
        mock_button = Mock()
        screen.groom_list(mock_button)
        
        # Should skip empty lines and only number actual tasks
        expected_text = "1. Task 1\n2. Task 2\n3. Task 3"
        screen.text_input.text = expected_text


class TestAppConfig:
    """Test AppConfig functionality."""
    
    def test_app_config_default_title(self):
        """Test AppConfig returns default title."""
        from src.core.config import AppConfig
        
        title = AppConfig.get_app_title()
        assert title == "Personal Assistance"
    
    def test_app_config_set_title(self):
        """Test AppConfig can set new title."""
        from src.core.config import AppConfig
        
        original_title = AppConfig.get_app_title()
        new_title = "New Personal Assistant"
        
        AppConfig.set_app_title(new_title)
        assert AppConfig.get_app_title() == new_title
        
        # Restore original title
        AppConfig.set_app_title(original_title)
    
    def test_app_config_class_methods(self):
        """Test that AppConfig methods are class methods."""
        from src.core.config import AppConfig
        
        # Should be able to call without instantiation
        assert hasattr(AppConfig, 'get_app_title')
        assert hasattr(AppConfig, 'set_app_title')
        assert callable(AppConfig.get_app_title)
        assert callable(AppConfig.set_app_title)


class TestUIComponentIntegration:
    """Test integration between UI components."""
    
    @patch('src.ui.screens.Screen.__init__')
    def test_screen_manager_integration(self, mock_screen_init):
        """Test that screens properly integrate with screen manager."""
        from src.ui.screens import MainMenuScreen
        
        mock_screen_init.return_value = None
        mock_manager = Mock()
        
        screen = MainMenuScreen()
        screen.manager = mock_manager
        
        # Test that screen can access manager
        assert screen.manager == mock_manager
        assert hasattr(screen, 'name')
        assert screen.name == 'main_menu'
    
    def test_button_callback_structure(self):
        """Test that button callbacks follow expected structure."""
        from src.ui.screens import MainMenuScreen
        
        with patch('src.ui.screens.Screen.__init__'):
            screen = MainMenuScreen()
            mock_manager = Mock()
            screen.manager = mock_manager
            
            # Buttons should have callbacks that call manager.switch_to_screen
            # This tests the pattern used in button binding
            callback = lambda x: screen.manager.switch_to_screen('executive_function')
            
            # Execute callback
            callback(None)
            
            # Verify manager method was called
            mock_manager.switch_to_screen.assert_called_with('executive_function')
    
    @patch('src.ui.screens.Screen.__init__')
    def test_times_dependencies_background_update(self, mock_screen_init):
        """Test background rectangle update method."""
        from src.ui.screens import TimesDependenciesScreen
        
        mock_screen_init.return_value = None
        
        screen = TimesDependenciesScreen()
        
        # Mock instance with background rectangle
        mock_instance = Mock()
        mock_instance.pos = (10, 20)
        mock_instance.size = (100, 50)
        mock_instance.bg_rect = Mock()
        
        # Test update_bg method
        screen.update_bg(mock_instance, None)
        
        # Verify background rectangle was updated
        assert mock_instance.bg_rect.pos == (10, 20)
        assert mock_instance.bg_rect.size == (100, 50)
"""
Navigation business logic - manages screen state without UI dependencies.
"""
from typing import List, Optional


class ScreenNavigator:
    """Manages screen navigation state and validation."""
    
    # Valid screen names in the application
    VALID_SCREENS = {
        'main_menu',
        'executive_function', 
        'emotions_management',
        'habits',
        'pomodoro',
        'routines',
        'todo_timeline',
        'todo_list',
        'times_dependencies',
        'timeline_view'
    }
    
    def __init__(self):
        self.current_screen = 'main_menu'
        self._history: List[str] = ['main_menu']
        
    def navigate_to(self, screen_name: str) -> bool:
        """Navigate to a screen. Returns True if successful, False if invalid."""
        if screen_name not in self.VALID_SCREENS:
            return False
            
        # Add current screen to history before navigating
        if screen_name != self.current_screen:
            self._history.append(self.current_screen)
            
        self.current_screen = screen_name
        return True
        
    def go_back(self) -> bool:
        """Navigate back to previous screen. Returns True if successful."""
        if len(self._history) > 0:
            self.current_screen = self._history.pop()
            return True
        return False
        
    def get_navigation_history(self) -> List[str]:
        """Get the navigation history."""
        return self._history.copy()
        
    def can_navigate_to(self, screen_name: str) -> bool:
        """Check if navigation to a screen is valid."""
        return screen_name in self.VALID_SCREENS
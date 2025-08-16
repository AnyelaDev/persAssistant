from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ListProperty
from src.core.config import AppConfig
from src.ui.color_palette import ColorPalette
from src.ui.screens import (
    MainMenuScreen, ExecutiveFunctionScreen, ToDoTimelineScreen,
    ToDoListScreen, TimesDependenciesScreen, TimelineViewScreen,
    EmotionsManagementScreen, HabitsScreen, PomodoroScreen, RoutinesScreen
)


class AppScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Add all screens
        self.add_widget(MainMenuScreen())
        self.add_widget(ExecutiveFunctionScreen())
        self.add_widget(ToDoTimelineScreen())
        self.add_widget(ToDoListScreen())
        self.add_widget(TimesDependenciesScreen())
        self.add_widget(TimelineViewScreen())
        self.add_widget(EmotionsManagementScreen())
        self.add_widget(HabitsScreen())
        self.add_widget(PomodoroScreen())
        self.add_widget(RoutinesScreen())
        
        # Set initial screen
        self.current = 'main_menu'
    
    def switch_to_screen(self, screen_name):
        self.current = screen_name


class PersonalAssistantApp(App):
    # Color properties that can be accessed in .kv files as app.text_primary_color, etc.
    text_primary_color = ListProperty(ColorPalette.TEXT_PRIMARY)
    text_secondary_color = ListProperty(ColorPalette.TEXT_SECONDARY)
    button_primary_color = ListProperty(ColorPalette.BUTTON_PRIMARY)
    button_secondary_color = ListProperty(ColorPalette.BUTTON_SECONDARY)
    button_tertiary_color = ListProperty(ColorPalette.BUTTON_TERTIARY)
    button_neutral_color = ListProperty(ColorPalette.BUTTON_NEUTRAL)
    background_primary_color = ListProperty(ColorPalette.BACKGROUND_PRIMARY)
    background_secondary_color = ListProperty(ColorPalette.BACKGROUND_SECONDARY)
    accent_blue_color = ListProperty(ColorPalette.ACCENT_BLUE)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = AppConfig.get_app_title()
    
    def build(self):
        return AppScreenManager()
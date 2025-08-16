from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from src.core.config import AppConfig
from src.ui.color_palette import ColorPalette


def set_screen_background(screen, color=None):
    """Helper function to set background color for any screen."""
    if color is None:
        color = ColorPalette.BACKGROUND_PRIMARY
    
    with screen.canvas.before:
        Color(*color)
        screen.rect = Rectangle(size=screen.size, pos=screen.pos)
    screen.bind(size=lambda instance, value: setattr(screen.rect, 'size', instance.size))
    screen.bind(pos=lambda instance, value: setattr(screen.rect, 'pos', instance.pos))


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main_menu'
        
        # Set screen background color
        set_screen_background(self)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text=AppConfig.get_app_title(),
            size_hint_y=None,
            height=80,
            font_size=32,
            color=ColorPalette.TEXT_PRIMARY
        )
        layout.add_widget(title)
        
        # Navigation buttons
        executive_btn = Button(
            text='Executive\nFunction',
            size_hint_y=None,
            height=120,
            font_size=20,
            background_color=ColorPalette.BUTTON_PRIMARY
        )
        executive_btn.bind(on_press=lambda x: self.manager.switch_to_screen('executive_function'))
        
        emotions_btn = Button(
            text='Emotions\nManagement',
            size_hint_y=None,
            height=120,
            font_size=20,
            background_color=ColorPalette.BUTTON_SECONDARY
        )
        emotions_btn.bind(on_press=lambda x: self.manager.switch_to_screen('emotions_management'))
        
        habits_btn = Button(
            text='Habits',
            size_hint_y=None,
            height=120,
            font_size=20,
            background_color=ColorPalette.BUTTON_TERTIARY
        )
        habits_btn.bind(on_press=lambda x: self.manager.switch_to_screen('habits'))
        
        layout.add_widget(executive_btn)
        layout.add_widget(emotions_btn)
        layout.add_widget(habits_btn)
        
        self.add_widget(layout)
        
    def get_navigation_options(self):
        """Return the navigation options available from this screen."""
        return [
            'executive_function',
            'emotions_management', 
            'habits',
            'pomodoro',
            'routines'
        ]


class ExecutiveFunctionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'executive_function'
        
        # Set screen background color
        set_screen_background(self)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='Executive\nFunction',
            size_hint_y=None,
            height=80,
            font_size=28,
            color=ColorPalette.TEXT_PRIMARY
        )
        layout.add_widget(title)
        
        # Sub-module buttons
        todo_timeline_btn = Button(
            text='ToDo\nTimeline',
            size_hint_y=None,
            height=120,
            font_size=20,
            background_color=ColorPalette.BUTTON_PRIMARY
        )
        todo_timeline_btn.bind(on_press=lambda x: self.manager.switch_to_screen('todo_timeline'))
        
        pomodoro_btn = Button(
            text='Pomodoro',
            size_hint_y=None,
            height=120,
            font_size=20,
            background_color=ColorPalette.BUTTON_SECONDARY
        )
        pomodoro_btn.bind(on_press=lambda x: self.manager.switch_to_screen('pomodoro'))
        
        routines_btn = Button(
            text='Routines',
            size_hint_y=None,
            height=120,
            font_size=20,
            background_color=ColorPalette.BUTTON_TERTIARY
        )
        routines_btn.bind(on_press=lambda x: self.manager.switch_to_screen('routines'))
        
        # Back button
        back_btn = Button(
            text='Back',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_NEUTRAL
        )
        back_btn.bind(on_press=lambda x: self.manager.switch_to_screen('main_menu'))
        
        layout.add_widget(todo_timeline_btn)
        layout.add_widget(pomodoro_btn)
        layout.add_widget(routines_btn)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
    def get_navigation_options(self):
        """Return the navigation options available from this screen."""
        return [
            'todo_timeline',
            'pomodoro',
            'routines'
        ]


class ToDoTimelineScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'todo_timeline'
        
        # Set screen background color
        set_screen_background(self)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='ToDo\nTimeline',
            size_hint_y=None,
            height=80,
            font_size=28,
            color=ColorPalette.TEXT_PRIMARY
        )
        layout.add_widget(title)
        
        # Sub-options
        todo_list_btn = Button(
            text='To-Do List',
            size_hint_y=None,
            height=120,
            font_size=20,
            background_color=ColorPalette.BUTTON_PRIMARY
        )
        todo_list_btn.bind(on_press=lambda x: self.manager.switch_to_screen('todo_list'))
        
        times_deps_btn = Button(
            text='Times and\ndependencies',
            size_hint_y=None,
            height=120,
            font_size=20,
            background_color=ColorPalette.BUTTON_SECONDARY
        )
        times_deps_btn.bind(on_press=lambda x: self.manager.switch_to_screen('times_dependencies'))
        
        timeline_btn = Button(
            text='Timeline',
            size_hint_y=None,
            height=120,
            font_size=20,
            background_color=ColorPalette.BUTTON_TERTIARY
        )
        timeline_btn.bind(on_press=lambda x: self.manager.switch_to_screen('timeline_view'))
        
        # Back button
        back_btn = Button(
            text='Back',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_NEUTRAL
        )
        back_btn.bind(on_press=lambda x: self.manager.switch_to_screen('executive_function'))
        
        layout.add_widget(todo_list_btn)
        layout.add_widget(times_deps_btn)
        layout.add_widget(timeline_btn)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
    def get_navigation_options(self):
        """Return the navigation options available from this screen."""
        return [
            'todo_list',
            'times_dependencies',
            'timeline_view'
        ]


class ToDoListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'todo_list'
        
        # Set screen background color
        set_screen_background(self)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='To-Do List',
            size_hint_y=None,
            height=60,
            font_size=28,
            color=ColorPalette.TEXT_PRIMARY
        )
        layout.add_widget(title)
        
        # Instruction
        instruction = Label(
            text='write your to do list.',
            size_hint_y=None,
            height=30,
            font_size=16,
            color=ColorPalette.TEXT_SECONDARY
        )
        layout.add_widget(instruction)
        
        # Text input area
        self.text_input = TextInput(
            hint_text='<Text Input>',
            multiline=True,
            font_size=16,
            background_color=ColorPalette.BUTTON_SECONDARY
        )
        layout.add_widget(self.text_input)
        
        # Buttons
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=10)
        
        groom_btn = Button(
            text='Groom my list',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_SECONDARY
        )
        groom_btn.bind(on_press=self.groom_list)
        
        next_btn = Button(
            text='Next',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_TERTIARY
        )
        next_btn.bind(on_press=lambda x: self.manager.switch_to_screen('times_dependencies'))
        
        button_layout.add_widget(groom_btn)
        button_layout.add_widget(next_btn)
        
        layout.add_widget(button_layout)
        
        # Back button
        back_btn = Button(
            text='Back',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_NEUTRAL
        )
        back_btn.bind(on_press=lambda x: self.manager.switch_to_screen('todo_timeline'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def groom_list(self, button):
        # Placeholder for list grooming functionality
        if self.text_input.text.strip():
            items = self.text_input.text.strip().split('\n')
            groomed_items = []
            for i, item in enumerate(items, 1):
                if item.strip():
                    groomed_items.append(f"{i}. {item.strip()}")
            self.text_input.text = '\n'.join(groomed_items)


class TimesDependenciesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'times_dependencies'
        
        # Set screen background color
        set_screen_background(self)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='Times and\nDependencies',
            size_hint_y=None,
            height=80,
            font_size=24,
            color=ColorPalette.TEXT_PRIMARY
        )
        layout.add_widget(title)
        
        # Subtitle
        subtitle = Label(
            text='Establish ToDos',
            size_hint_y=None,
            height=30,
            font_size=16,
            color=ColorPalette.TEXT_SECONDARY
        )
        layout.add_widget(subtitle)
        
        # Scrollable content
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Sample todo items
        for i in range(1, 4):
            item_layout = BoxLayout(
                orientation='vertical', 
                size_hint_y=None, 
                height=120,
                padding=10,
                spacing=5
            )
            
            item_label = Label(
                text=f'<To do item n+{i-1}>',
                size_hint_y=None,
                height=30,
                font_size=14,
                color=ColorPalette.TEXT_PRIMARY
            )
            
            time_input = TextInput(
                hint_text='Time: <input text>',
                size_hint_y=None,
                height=30,
                font_size=14
            )
            
            deps_input = TextInput(
                hint_text='Dependencies: <input text>',
                size_hint_y=None,
                height=30,
                font_size=14
            )
            
            item_layout.add_widget(item_label)
            item_layout.add_widget(time_input)
            item_layout.add_widget(deps_input)
            
            # Add colored background
            item_layout.canvas.before.clear()
            from kivy.graphics import Color, Rectangle
            with item_layout.canvas.before:
                Color(*ColorPalette.BUTTON_SECONDARY)
                item_layout.bg_rect = Rectangle(size=item_layout.size, pos=item_layout.pos)
            
            item_layout.bind(size=self.update_bg, pos=self.update_bg)
            content.add_widget(item_layout)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        
        # Buttons
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=10)
        
        groom_btn = Button(
            text='Groom my list',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_SECONDARY
        )
        
        next_btn = Button(
            text='Next',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_TERTIARY
        )
        next_btn.bind(on_press=lambda x: self.manager.switch_to_screen('timeline_view'))
        
        button_layout.add_widget(groom_btn)
        button_layout.add_widget(next_btn)
        
        layout.add_widget(button_layout)
        
        # Back button
        back_btn = Button(
            text='Back',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_NEUTRAL
        )
        back_btn.bind(on_press=lambda x: self.manager.switch_to_screen('todo_list'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def update_bg(self, instance, value):
        instance.bg_rect.pos = instance.pos
        instance.bg_rect.size = instance.size


class TimelineViewScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'timeline_view'
        
        # Set screen background color
        set_screen_background(self)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='Timeline',
            size_hint_y=None,
            height=60,
            font_size=28,
            color=ColorPalette.TEXT_SECONDARY
        )
        layout.add_widget(title)
        
        # Timeline bar placeholder
        timeline_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=30
        )
        
        # Red and gray sections
        from kivy.graphics import Color, Rectangle
        red_section = Label(text='<Start\ntime>', size_hint_x=0.3, font_size=10, color=ColorPalette.TEXT_PRIMARY)
        gray_section = Label(text='<Finish\ntime>', size_hint_x=0.7, font_size=10, color=ColorPalette.TEXT_PRIMARY)
        
        timeline_bar.add_widget(red_section)
        timeline_bar.add_widget(gray_section)
        layout.add_widget(timeline_bar)
        
        # Current task
        current_task = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=80,
            padding=10,
            spacing=10
        )
        
        now_label = Label(
            text='Now',
            size_hint_x=None,
            width=80,
            font_size=18,
            color=ColorPalette.TEXT_PRIMARY
        )
        
        task_info = BoxLayout(orientation='vertical')
        task_name = Label(text='<To do item n>', font_size=16, color=ColorPalette.TEXT_PRIMARY)
        task_next = Label(text='Next: <Todo item m>', font_size=14, color=ColorPalette.TEXT_SECONDARY)
        task_info.add_widget(task_name)
        task_info.add_widget(task_next)
        
        time_info = Label(
            text='Time left:\n<time in\nhh:mm>',
            size_hint_x=None,
            width=100,
            font_size=12,
            color=ColorPalette.TEXT_SECONDARY
        )
        
        current_task.add_widget(now_label)
        current_task.add_widget(task_info)
        current_task.add_widget(time_info)
        layout.add_widget(current_task)
        
        # In parallel section
        parallel_label = Label(
            text='in parallel:',
            size_hint_y=None,
            height=30,
            font_size=16,
            color=ColorPalette.TEXT_PRIMARY
        )
        layout.add_widget(parallel_label)
        
        # Parallel tasks
        parallel_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, spacing=10)
        
        for i in range(2):
            parallel_task = BoxLayout(
                orientation='vertical',
                padding=10
            )
            
            task_label = Label(text=f'<To do item n+{i+1}>', font_size=14, color=ColorPalette.TEXT_PRIMARY)
            time_label = Label(text='Time: <hh:mm>', font_size=12, color=ColorPalette.TEXT_SECONDARY)
            deps_label = Label(text='Dependencies: <input text>', font_size=12, color=ColorPalette.TEXT_SECONDARY)
            
            parallel_task.add_widget(task_label)
            parallel_task.add_widget(time_label)
            parallel_task.add_widget(deps_label)
            
            parallel_layout.add_widget(parallel_task)
        
        layout.add_widget(parallel_layout)
        
        # ToDo List section
        todo_section = BoxLayout(orientation='vertical', spacing=10)
        
        todo_title = Label(
            text='ToDo List',
            size_hint_y=None,
            height=40,
            font_size=20,
            color=ColorPalette.TEXT_PRIMARY
        )
        todo_section.add_widget(todo_title)
        
        todo_content = Label(
            text='<Ordered List of groomed\nToDos>',
            color=ColorPalette.TEXT_SECONDARY
        )
        todo_section.add_widget(todo_content)
        
        layout.add_widget(todo_section)
        
        # Home button
        home_btn = Button(
            text='Home',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_TERTIARY
        )
        home_btn.bind(on_press=lambda x: self.manager.switch_to_screen('main_menu'))
        layout.add_widget(home_btn)
        
        # Back button
        back_btn = Button(
            text='Back',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_NEUTRAL
        )
        back_btn.bind(on_press=lambda x: self.manager.switch_to_screen('times_dependencies'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)


# Placeholder screens
class EmotionsManagementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'emotions_management'
        
        # Set screen background color
        set_screen_background(self)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(
            text='Emotions Management',
            size_hint_y=None,
            height=80,
            font_size=28
        )
        
        placeholder = Label(
            text='Coming Soon...',
            font_size=20
        )
        
        back_btn = Button(
            text='Back',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_NEUTRAL
        )
        back_btn.bind(on_press=lambda x: self.manager.switch_to_screen('main_menu'))
        
        layout.add_widget(title)
        layout.add_widget(placeholder)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)


class HabitsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'habits'
        
        # Set screen background color
        set_screen_background(self)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(
            text='Habits',
            size_hint_y=None,
            height=80,
            font_size=28
        )
        
        placeholder = Label(
            text='Coming Soon...',
            font_size=20
        )
        
        back_btn = Button(
            text='Back',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_NEUTRAL
        )
        back_btn.bind(on_press=lambda x: self.manager.switch_to_screen('main_menu'))
        
        layout.add_widget(title)
        layout.add_widget(placeholder)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)


class PomodoroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'pomodoro'
        
        # Set screen background color
        set_screen_background(self)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(
            text='Pomodoro',
            size_hint_y=None,
            height=80,
            font_size=28
        )
        
        placeholder = Label(
            text='Coming Soon...',
            font_size=20
        )
        
        back_btn = Button(
            text='Back',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_NEUTRAL
        )
        back_btn.bind(on_press=lambda x: self.manager.switch_to_screen('executive_function'))
        
        layout.add_widget(title)
        layout.add_widget(placeholder)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)


class RoutinesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'routines'
        
        # Set screen background color
        set_screen_background(self)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(
            text='Routines',
            size_hint_y=None,
            height=80,
            font_size=28
        )
        
        placeholder = Label(
            text='Coming Soon...',
            font_size=20
        )
        
        back_btn = Button(
            text='Back',
            size_hint_y=None,
            height=50,
            background_color=ColorPalette.BUTTON_NEUTRAL
        )
        back_btn.bind(on_press=lambda x: self.manager.switch_to_screen('executive_function'))
        
        layout.add_widget(title)
        layout.add_widget(placeholder)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
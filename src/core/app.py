from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        # Title
        title = Label(
            text='Personal Assistant',
            size_hint_y=None,
            height=50,
            font_size=24
        )
        self.add_widget(title)
        
        # Input area
        self.text_input = TextInput(
            hint_text='How can I help you today?',
            multiline=True,
            size_hint_y=None,
            height=100
        )
        self.add_widget(self.text_input)
        
        # Send button
        send_btn = Button(
            text='Send',
            size_hint_y=None,
            height=50
        )
        send_btn.bind(on_press=self.on_send)
        self.add_widget(send_btn)
        
        # Response area
        self.response_label = Label(
            text='Welcome! I\'m your personal assistant.',
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        self.add_widget(self.response_label)
    
    def on_send(self, button):
        user_input = self.text_input.text
        if user_input.strip():
            self.response_label.text = f"You said: {user_input}"
            self.text_input.text = ""


class PersonalAssistantApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Personal Assistant'
    
    def build(self):
        return MainWidget()
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from ui.customWordInput import CustomWordInput
from ui.eventHandlers import EventHandlers

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.WordSolver = None  # Inicjalizacja WordSolver jako None
        with open('./Data/slowa.txt', 'r', encoding='utf-8') as file:
            self.words = file.readlines()
        self.word_list = TextInput(hint_text='Wyświetlane słowa', multiline=True, readonly=True, size_hint=(0.9, 0.95)  )
        self.letters_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.in_letters_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.selected_number = None
        self.word1 = CustomWordInput(
            app_instance=self,
            input_callback=None,
            delete_callback=None,
            hint_text='Wpisz Litery',
            multiline=False,
            size_hint_y=None,
            height=30
        )
        self.word1_box = BoxLayout(orientation='vertical', size_hint_y=None, height=50)
        #Visibility
        self.word1_box.opacity = 0
        self.word1_box.disabled = True
        self.correct_letters_box = BoxLayout(orientation='vertical', size_hint_y=None, height=50)
        self.correct_letters_box.opacity = 0
        self.correct_letters_box.disabled = True
        self.incorrect_letters_box = BoxLayout(orientation='vertical', size_hint_y=None, height=50)
        self.incorrect_letters_box.opacity = 0
        self.incorrect_letters_box.disabled = True
        self.eventHandlers = EventHandlers(self.WordSolver, self.word_list, self.letters_layout, self.in_letters_layout, self.selected_number, self.words, self.word1, self.word1_box, self.correct_letters_box, self.incorrect_letters_box )
        self.word1.input_callback=self.eventHandlers.on_word1_input
        self.word1.delete_callback=self.eventHandlers.on_word1_delete
        
    def build(self):
        self.title = "Wordle Solver"  # Set the window title
        
        root_layout = BoxLayout(orientation='vertical', padding=[10, 10, 10, 0])

        top_layout = BoxLayout(orientation='vertical', padding=10, spacing=5, size_hint_y=None)
        top_layout.bind(minimum_height= top_layout.setter('height'))
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=44)
        
        self.clear_button = Button(
            text="Wyczyść",
            size_hint=(None, None),
            size=(100, 44),
            on_press=self.eventHandlers.clear_all_inputs
        )
        button_layout.add_widget(self.clear_button)

        self.spinner_layout = AnchorLayout(anchor_x='right', anchor_y='top')
        self.spinner = Spinner(
            text='Wybierz liczbę',
            values=[str(i) for i in range(2, 12)],
            size_hint=(None, None),
            size=(100, 44)
        )
        self.spinner.bind(text=self.eventHandlers.on_spinner_select)
        self.spinner_layout.add_widget(self.spinner)
        button_layout.add_widget(self.spinner_layout)
        
        top_layout.add_widget(button_layout)

        #Word1 Label 
        self.word1_label = Label(text='Litery których nie ma w słowie', size_hint_y=None, height=20, halign='left', valign='middle')
        self.word1_label.bind(size=self.word1_label.setter('text_size'))
        self.word1_box.add_widget(self.word1_label)
        self.word1_box.add_widget(self.word1)

        top_layout.add_widget(self.word1_box)

        self.correct_letters_label = Label(text='Litery na poprawnych pozycjach', size_hint_y=None, height=20, halign='left', valign='middle')
        self.correct_letters_box.add_widget(self.correct_letters_label)

        top_layout.add_widget(self.correct_letters_box)

        #Letters input
        self.letters_layout.bind(minimum_height=self.letters_layout.setter('height'))
        self.letters_layout.size_hint_y = None
        self.letters_layout.height = 60
        top_layout.add_widget(self.letters_layout)

        self.incorrect_letters_label = Label(text='Litery na niepoprawnych pozycjach', size_hint_y=None, height=20, halign='left', valign='middle')
        self.incorrect_letters_box.add_widget(self.incorrect_letters_label)

        top_layout.add_widget(self.incorrect_letters_box)

        #Letters input
        self.in_letters_layout.bind(minimum_height=self.in_letters_layout.setter('height'))
        self.in_letters_layout.size_hint_y = None
        self.in_letters_layout.height = 60
        top_layout.add_widget(self.in_letters_layout)

        root_layout.add_widget(top_layout)
        
        bottom_layout = BoxLayout(size_hint_y=0.5, padding=[10, 0, 10, 10])
        bottom_layout.add_widget(self.word_list)
        
        root_layout.add_widget(bottom_layout)

        return root_layout

    

if __name__ == "__main__":
    MyApp().run()
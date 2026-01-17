from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.metrics import dp, Metrics
from kivy.clock import Clock
from ui.styles import COLORS, FONTS
from ui.customWordInput import CustomWordInput
from ui.eventHandlers import EventHandlers
from ui.styledButton import StyledButton
from ui.styledSpinner import StyledSpinner
from ui.styledTextInput import StyledTextInput
from ui.limitedTextInput import LimitedTextInput
from ui.limitedTextInputNotOnPosition import LimitedTextInputNotOnPosition
from kivy.storage.jsonstore import JsonStore


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.store = JsonStore('config.json')
        
        if self.store.exists('display'):
            saved_density = self.store.get('display')['density']
            Metrics.density = float(saved_density)
        else:
            Metrics.density = 1.2 
            self.store.put('display', density=1.2)

        Window.clearcolor = COLORS["background"]
        self.title = "Wordle Solver - Premium"
        Window.size = (1000, 800)

        self.top_layout = None
        self.results_label = None
        self.WordSolver = None
        self.current_word_length = None
        
        try:
            with open("../Data/slowa.txt", "r", encoding="utf-8") as file:
                self.words = file.readlines()
        except FileNotFoundError:
            print("Błąd: Nie znaleziono pliku ../Data/slowa.txt")
            self.words = []

    def build(self):
        self.root_layout = BoxLayout(
            orientation="vertical",
            padding=[dp(15), dp(15), dp(15), dp(10)],
            spacing=dp(10),
        )
        self.create_interface()
        Clock.schedule_once(self.resize_window, 0.1)
        return self.root_layout

    def reload_interface(self, new_density):
        saved_excluded = self.word1.text
        saved_grid_texts = []
        if hasattr(self, 'eventHandlers') and self.eventHandlers.letter_inputs:
            saved_grid_texts = [inp.text for inp in self.eventHandlers.letter_inputs]

        Metrics.density = new_density
        self.root_layout.clear_widgets()
        self.create_interface()
        
        if hasattr(self, 'eventHandlers'):
            self.eventHandlers.is_restoring = True
            
            if saved_excluded:
                self.word1.text = saved_excluded
                self.eventHandlers.on_word1_input(self.word1, saved_excluded)
                
            if len(self.eventHandlers.letter_inputs) == len(saved_grid_texts):
                for i, text in enumerate(saved_grid_texts):
                    if text:
                        inp = self.eventHandlers.letter_inputs[i]
                        inp.text = text
                        if isinstance(inp, LimitedTextInput):
                            self.eventHandlers.on_letter_input(inp)
                        elif isinstance(inp, LimitedTextInputNotOnPosition):
                            self.eventHandlers.on_letter_input_not_on_pos(inp, text)
            
            self.eventHandlers.is_restoring = False
            self.eventHandlers.trigger_search()

        Clock.schedule_once(self.resize_window, 0.1)

    def resize_window(self, dt):
        if not self.top_layout or not self.results_label:
            return

        self.root_layout.do_layout()
        
        min_list_height = dp(250)
        required_height = (
            self.top_layout.minimum_height + 
            self.results_label.height + 
            min_list_height + 
            dp(50)
        )
        
        min_width = dp(700)
        current_width, current_height = Window.size
        
        Window.minimum_width = min_width
        Window.minimum_height = required_height
        
        target_width = max(current_width, min_width)
        target_height = max(current_height, required_height)
        
        if current_width < min_width or current_height < required_height:
            Window.size = (target_width, target_height)

    def create_interface(self):
        self.word_list = StyledTextInput(
            hint_text="Znalezione słowa będą wyświetlane tutaj",
            multiline=True,
            readonly=True,
            hint_text_color=COLORS["primary"],
            size_hint=(1, 1),
            background_disabled_normal="",
        )
        self.word_list.write_tab = False
        self.word_list.cursor_blink = False
        self.word_list.cursor_width = 0

        self.letters_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        self.in_letters_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        
        self.selected_number = self.current_word_length

        self.word1 = CustomWordInput(
            app_instance=self,
            input_callback=None,
            delete_callback=None,
            hint_text="Wpisz litery",
            cursor_color=COLORS["primary"],
            hint_text_color=COLORS["hint"],
            foreground_color=COLORS["text"],
            font_size=dp(16),
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_name=FONTS["regular"],
            background_color=COLORS["surface"],
        )

        self.init_containers()

        self.eventHandlers = EventHandlers(
            self.WordSolver,
            self.word_list,
            self.letters_layout,
            self.in_letters_layout,
            self.selected_number,
            self.words,
            self.word1,
            self.word1_box,
            self.correct_letters_box,
            self.incorrect_letters_box,
            COLORS,
            self.store,
            self 
        )
        
        self.word1.input_callback = self.eventHandlers.on_word1_input
        self.word1.delete_callback = self.eventHandlers.on_word1_delete

        self.top_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(20),
            size_hint_y=None,
        )
        self.top_layout.bind(minimum_height=self.top_layout.setter("height"))

        control_panel = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
        )

        self.clear_button = StyledButton(
            text="Wyczyść", size_hint=(0.3, None), height=dp(50)
        )
        self.clear_button.bind(on_press=self.eventHandlers.clear_all_inputs)

        self.spinner = StyledSpinner(
            text="Długość",
            values=[str(i) for i in range(2, 12)],
            size_hint=(0.35, None),
            height=dp(50),
        )
        self.spinner.bind(text=self.eventHandlers.on_spinner_select)
        
        scale_values = ['1.0', '1.25', '1.5', '1.75', '2.0']
        formatted_values = [f"Skala: {v}" for v in scale_values]
        
        self.scale_spinner = StyledSpinner(
            text=f"Skala: {Metrics.density:.2f}",
            values=formatted_values,
            size_hint=(0.35, None),
            height=dp(50),
        )
        self.scale_spinner.bind(text=self.eventHandlers.on_scale_select)

        control_panel.add_widget(self.clear_button)
        control_panel.add_widget(self.spinner)
        control_panel.add_widget(self.scale_spinner)
        self.top_layout.add_widget(control_panel)

        sections = [
            ("Litery wykluczone", self.word1_box, self.word1),
            ("Litery na pozycjach", self.correct_letters_box, self.letters_layout),
            ("Litery nie na pozycjach", self.incorrect_letters_box, self.in_letters_layout),
        ]

        for title, box, widget in sections:
            label = Label(
                text=title,
                color=COLORS["text"],
                font_name=FONTS["medium"],
                font_size=dp(16),
                size_hint_y=None,
                height=dp(25),
                halign="left",
            )
            label.bind(size=lambda instance, value: setattr(instance, "text_size", value))

            box.clear_widgets()
            box.add_widget(label)
            if widget.parent:
                widget.parent.remove_widget(widget)
            box.add_widget(widget)
            self.top_layout.add_widget(self.create_section_wrapper(box))

        self.results_label = Label(
            text="Proponowane rozwiązania:",
            color=COLORS["text"],
            font_name=FONTS["medium"],
            font_size=dp(16),
            size_hint_y=None,
            height=dp(25),
            halign="left",
        )
        self.results_label.bind(size=self.results_label.setter("text_size"))

        self.root_layout.add_widget(self.top_layout)
        self.root_layout.add_widget(self.results_label)
        
        if self.word_list.parent:
            self.word_list.parent.remove_widget(self.word_list)
        self.root_layout.add_widget(self.word_list)

        if self.current_word_length:
            self.spinner.text = str(self.current_word_length)
            self.eventHandlers.on_spinner_select(self.spinner, str(self.current_word_length))

    def init_containers(self):
        self.create_box = lambda: BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(5),
            padding=[0, dp(10), 0, 0],
        )

        self.word1_box = self.create_box()
        self.correct_letters_box = self.create_box()
        self.incorrect_letters_box = self.create_box()

        for box in [self.word1_box, self.correct_letters_box, self.incorrect_letters_box]:
            box.opacity = 0
            box.disabled = True

        self.word1_box.height = dp(80)
        self.correct_letters_box.height = dp(100)
        self.incorrect_letters_box.height = dp(100)

    def create_section_wrapper(self, content):
        wrapper = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=[dp(5), dp(5)],
            spacing=dp(5),
            height=content.height,
        )
        wrapper.add_widget(content)
        return wrapper


if __name__ == "__main__":
    MyApp().run()
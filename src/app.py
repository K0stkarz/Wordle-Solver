from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from ui.styles import COLORS, FONTS
from ui.customWordInput import CustomWordInput
from ui.eventHandlers import EventHandlers
from ui.styledButton import StyledButton
from ui.styledSpinner import StyledSpinner
from ui.styledTextInput import StyledTextInput


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.WordSolver = None
        with open("../Data/slowa.txt", "r", encoding="utf-8") as file:
            self.words = file.readlines()

        # Inicjalizacja pól tekstowych
        self.word_list = StyledTextInput(
            hint_text="Znalezione słowa będą wyświetlane tutaj",
            multiline=True,
            readonly=True,
            hint_text_color=COLORS["primary"],
            size_hint=(1, 1),
            background_disabled_normal="",  # Wyłącz domyślny styl disabled
        )
        self.word_list.write_tab = False
        self.word_list.cursor_blink = False
        self.word_list.cursor_width = 0

        # Layouty
        self.letters_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        self.in_letters_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        self.selected_number = None

        # Custom input
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

        # Kontenery
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
        )
        self.word1.input_callback = self.eventHandlers.on_word1_input
        self.word1.delete_callback = self.eventHandlers.on_word1_delete

    def init_containers(self):
        # Kontenery z animowaną widocznością
        self.create_box = lambda: BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(5),
            padding=[0, dp(10), 0, 0],
        )

        self.word1_box = self.create_box()
        self.correct_letters_box = self.create_box()
        self.incorrect_letters_box = self.create_box()

        for box in [
            self.word1_box,
            self.correct_letters_box,
            self.incorrect_letters_box,
        ]:
            box.opacity = 0
            box.disabled = True

        self.word1_box.height = dp(80)
        self.correct_letters_box.height = dp(100)
        self.incorrect_letters_box.height = dp(100)

    def build(self):
        Window.clearcolor = COLORS["background"]
        self.title = "Wordle Solver - Premium"

        # Główny layout
        root_layout = BoxLayout(
            orientation="vertical",
            padding=[dp(15), dp(15), dp(15), dp(10)],
            spacing=dp(10),
        )

        # Górna sekcja
        top_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(20),
            size_hint_y=None,
        )
        top_layout.bind(minimum_height=top_layout.setter("height"))

        # Panel sterowania
        control_panel = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
        )

        # Przycisk czyszczenia
        self.clear_button = StyledButton(
            text="Wyczyść wszystko", size_hint=(0.4, None), height=dp(50)
        )
        self.clear_button.bind(on_press=self.eventHandlers.clear_all_inputs)

        # Spinner długości słowa
        self.spinner = StyledSpinner(
            text="Długość słowa",
            values=[str(i) for i in range(2, 12)],
            size_hint=(0.6, None),
            height=dp(50),
        )
        self.spinner.bind(text=self.eventHandlers.on_spinner_select)

        control_panel.add_widget(self.clear_button)
        control_panel.add_widget(self.spinner)
        top_layout.add_widget(control_panel)

        # Sekcje wejściowe
        sections = [
            ("Litery wykluczone", self.word1_box, self.word1),
            ("Litery na pozycjach", self.correct_letters_box, self.letters_layout),
            (
                "Litery nie na pozycjach",
                self.incorrect_letters_box,
                self.in_letters_layout,
            ),
        ]

        for title, box, widget in sections:
            # Nagłówek sekcji
            label = Label(
                text=title,
                color=COLORS["text"],
                font_name=FONTS["medium"],
                font_size=dp(16),
                size_hint_y=None,
                height=dp(25),
                halign="left",
            )
            label.bind(
                size=lambda instance, value: setattr(instance, "text_size", value)
            )

            # Kontener
            box.add_widget(label)
            if widget:
                if isinstance(widget, GridLayout):
                    box.add_widget(widget)
                else:
                    box.add_widget(widget)

            top_layout.add_widget(self.create_section_wrapper(box))

        # Lista wyników
        results_label = Label(
            text="Proponowane rozwiązania:",
            color=COLORS["text"],
            font_name=FONTS["medium"],
            font_size=dp(16),
            size_hint_y=None,
            height=dp(25),
            halign="left",
        )
        results_label.bind(size=results_label.setter("text_size"))

        root_layout.add_widget(top_layout)
        root_layout.add_widget(results_label)
        root_layout.add_widget(self.word_list)

        return root_layout

    def _update_bg(self, instance, value):
        # Zapobiegaj pozostawaniu artefaktów
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*COLORS["background"])
            Rectangle(pos=instance.pos, size=instance.size)

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

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == "__main__":
    MyApp().run()

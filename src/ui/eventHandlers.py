import threading
from kivy.clock import mainthread, Clock
from kivy.metrics import Metrics
from . import (
    WordFinder,
    LimitedTextInput,
    Label,
    LimitedTextInputNotOnPosition,
    dp,
    BoxLayout
)

class EventHandlers:
    def __init__(
        self,
        word_solver: WordFinder,
        word_list,
        letters_layout,
        in_letters_layout,
        selected_number,
        words,
        word1,
        word1_box,
        correct_letters_box,
        incorrect_letters_box,
        COLORS,
        store,
        app,
    ):
        self.COLORS = COLORS
        self.WordSolver = word_solver
        self.word_list = word_list
        self.letters_layout = letters_layout
        self.in_letters_layout = in_letters_layout
        self.selected_number = selected_number
        self.letter_inputs = []
        self.words = words
        self.word1 = word1
        self.word1_box = word1_box
        self.correct_letters_box = correct_letters_box
        self.incorrect_letters_box = incorrect_letters_box
        self.store = store
        self.app = app
        
        # Flaga blokująca szukanie podczas przywracania stanu
        self.is_restoring = False
        # Timer do debouncingu (opóźnienia szukania)
        self.search_event = None

    def trigger_search(self):
        """Uruchamia szukanie z opóźnieniem (żeby nie mulić przy szybkim pisaniu)"""
        if self.search_event:
            self.search_event.cancel()
        # Czekaj 0.1s po ostatnim wciśnięciu klawisza zanim zaczniesz liczyć
        self.search_event = Clock.schedule_once(lambda dt: self._start_thread(), 0.1)

    def _start_thread(self):
        threading.Thread(target=self._run_search_background, daemon=True).start()

    def _run_search_background(self):
        if self.WordSolver:
            try:
                results = self.WordSolver.search()
                self._update_ui_results(results)
            except Exception as e:
                print(f"Błąd szukania: {e}")

    @mainthread
    def _update_ui_results(self, results):
        if not results:
            self.word_list.text = ""
            self.word_list.hint_text = "Brak wyników"
        else:
            self.word_list.text = "\n".join(results)
            self.word_list.hint_text = "Znalezione słowa..."

    def on_spinner_select(self, spinner, text):
        self.clear_all_inputs(None)
        
        for box in [self.word1_box, self.correct_letters_box, self.incorrect_letters_box]:
            box.opacity = 1
            box.disabled = False

        self.selected_number = int(text)
        
        # Zapisz wybór w App
        if self.app:
            self.app.current_word_length = self.selected_number
            
        self.WordSolver = WordFinder(self.selected_number, self.words)
        self._create_input_fields()
        
        # Wymuś odświeżenie widoku
        self.letters_layout.do_layout()
        self.in_letters_layout.do_layout()

    def on_scale_select(self, spinner, text):
        try:
            raw_value = text.replace("Skala: ", "")
            new_density = float(raw_value)
            
            if abs(new_density - Metrics.density) < 0.01:
                return

            if self.store:
                self.store.put('display', density=new_density)
            
            self.app.reload_interface(new_density)
            
        except ValueError:
            pass

    def _create_input_fields(self):
        self.letters_layout.clear_widgets()
        self.in_letters_layout.clear_widgets()
        self.letter_inputs = []

        for layout in [self.letters_layout, self.in_letters_layout]:
            layout.cols = self.selected_number
            layout.size_hint_y = None
            layout.height = dp(45)

        self._add_fields_to_layout(self.letters_layout, LimitedTextInput)
        self._add_fields_to_layout(self.in_letters_layout, LimitedTextInputNotOnPosition)

    def _add_fields_to_layout(self, layout, input_class):
        for i in range(1, self.selected_number + 1):
            box = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(60))

            if input_class == LimitedTextInputNotOnPosition:
                input_field = input_class(
                    app_instance=self,
                    max_length=self.selected_number,
                    background_color=self.COLORS["surface"],
                    cursor_color=self.COLORS["primary"],
                    hint_text_color=self.COLORS["hint"],
                    foreground_color=self.COLORS["text"],
                    hint_text="Wpisz literę",
                    multiline=False,
                    size_hint_y=None,
                    height=dp(30),
                )
            else:
                input_field = input_class(
                    app_instance=self,
                    background_color=self.COLORS["surface"],
                    cursor_color=self.COLORS["primary"],
                    hint_text_color=self.COLORS["hint"],
                    foreground_color=self.COLORS["text"],
                    hint_text="Wpisz literę",
                    multiline=False,
                    size_hint_y=None,
                    height=dp(30),
                )

            input_field.index = i - 1
            number_label = Label(
                text=str(i),
                color=self.COLORS["text"],
                size_hint_y=None,
                height=dp(20),
                halign="center",
                valign="middle",
            )
            number_label.bind(size=number_label.setter("text_size"))
            box.add_widget(input_field)
            box.add_widget(number_label)
            layout.add_widget(box)
            self.letter_inputs.append(input_field)

    def clear_all_inputs(self, instance):
        self.word1.text = ""
        self.word_list.text = ""
        if self.WordSolver is not None:
            self.WordSolver.letters = [None for _ in range(self.WordSolver.length)]
            self.WordSolver.lettersNoPos = []
            self.WordSolver.results = []
            self.WordSolver.positions = []
            self.WordSolver.noAvaliable = []
            self.WordSolver.notOnPosition = {}
        if hasattr(self, "letter_inputs"):
            for letter_input in self.letter_inputs:
                letter_input.text = ""

    def on_letter_input(self, text_input):
        letter = text_input.text
        position = text_input.index
        self.WordSolver.input(letter, position)
        if not self.is_restoring:
            self.trigger_search()

    def on_letter_delete(self, text_input):
        position = text_input.index
        if text_input.text == "":
            self.WordSolver.undo(position=position)
        if not self.is_restoring:
            self.trigger_search()

    def on_letter_input_not_on_pos(self, text_input, to_add):
        position = text_input.index
        self.WordSolver.input(to_add, notOnPosition=position - self.selected_number)
        if not self.is_restoring:
            self.trigger_search()

    def on_letter_delete_not_on_pos(self, text_input, to_del):
        self.WordSolver.undo(to_del, notOnPosition=text_input.index - self.selected_number)
        if not self.is_restoring:
            self.trigger_search()

    def on_word1_input(self, instance, value):
        for letter in value:
            if letter.isalpha():
                self.WordSolver.input(letter=letter, available=False)
        if not self.is_restoring:
            self.trigger_search()

    def on_word1_delete(self, instance):
        self.WordSolver.noAvaliable = []
        for letter in instance.text:
            if letter.isalpha():
                self.WordSolver.input(letter=letter, available=False)
        if not self.is_restoring:
            self.trigger_search()
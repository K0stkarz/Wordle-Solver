from . import (
    BoxLayout,
    WordFinder,
    LimitedTextInput,
    Label,
    LimitedTextInputNotOnPosition,
    dp,
    get_color_from_hex,
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

    def on_spinner_select(self, spinner, text):
        # Resetuj wszystkie pola
        self.clear_all_inputs(None)

        # Aktualizuj widoczność
        for box in [
            self.word1_box,
            self.correct_letters_box,
            self.incorrect_letters_box,
        ]:
            box.opacity = 1
            box.disabled = False

        # Pozostała logika
        self.selected_number = int(text)
        self.WordSolver = WordFinder(self.selected_number, self.words)
        self._create_input_fields()

        # Wymuś aktualizację layoutu
        self.letters_layout.do_layout()
        self.in_letters_layout.do_layout()

    def _create_input_fields(self):
        # Czyszczenie layoutów
        self.letters_layout.clear_widgets()
        self.in_letters_layout.clear_widgets()
        self.letter_inputs = []

        # Konfiguracja layoutów
        for layout in [self.letters_layout, self.in_letters_layout]:
            layout.cols = self.selected_number
            layout.size_hint_y = None
            layout.height = dp(45)  # Używaj dp dla spójności

        # Tworzenie pól wejściowych
        self._add_fields_to_layout(self.letters_layout, LimitedTextInput)
        self._add_fields_to_layout(
            self.in_letters_layout, LimitedTextInputNotOnPosition
        )

    def _add_fields_to_layout(self, layout, input_class):
        for i in range(1, self.selected_number + 1):
            box = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(60))

            # Tworzenie pola z odpowiednią klasą
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
        # Funkcja
        letter = text_input.text
        position = text_input.index

        # Wywołanie metody WordSolver.input z literą i pozycją
        self.WordSolver.input(letter, position)

        # Aktualizacja pola wyświetlania słów
        searchedWords = self.WordSolver.search()
        self.word_list.text = "\n".join(searchedWords)

    def on_letter_delete(self, text_input):
        # Funkcja wywoływana po skasowaniu litery

        self.word_list.text = ""

        position = text_input.index

        # Wywołanie metody WordSolver.undo z pozycją
        if text_input.text == "":
            self.WordSolver.undo(position=position)

        # Aktualizacja pola wyświetlania słów
        if (
            self.WordSolver.positions == []
            and self.WordSolver.letters == [None for _ in range(self.selected_number)]
            and self.WordSolver.noAvaliable == []
            and self.WordSolver.lettersNoPos == []
            and self.WordSolver.notOnPosition == {}
        ):
            self.word_list.text = ""
        else:
            searchedWords = self.WordSolver.search()
            self.word_list.text = "\n".join(searchedWords)

    def on_letter_input_not_on_pos(self, text_input, to_add):
        # Funkcja wywoływana po wpisaniu litery
        self.word_list.text = ""
        position = text_input.index

        # Wywołanie metody WordSolver.input z literą i pozycją
        self.WordSolver.input(to_add, notOnPosition=position - self.selected_number)

        # Aktualizacja pola wyświetlania słów
        searchedWords = self.WordSolver.search()
        self.word_list.text = "\n".join(searchedWords)

    def on_letter_delete_not_on_pos(self, text_input, to_del):
        # Funkcja wywoływana po skasowaniu litery

        self.word_list.text = ""

        self.WordSolver.undo(
            to_del, notOnPosition=text_input.index - self.selected_number
        )

        # Aktualizacja pola wyświetlania słów
        if (
            self.WordSolver.positions == []
            and self.WordSolver.letters == [None for _ in range(self.selected_number)]
            and self.WordSolver.noAvaliable == []
            and self.WordSolver.lettersNoPos == []
            and self.WordSolver.notOnPosition == {}
        ):
            self.word_list.text = ""
        else:
            searchedWords = self.WordSolver.search()
            self.word_list.text = "\n".join(searchedWords)

    def on_word1_input(self, instance, value):
        self.word_list.text = ""

        for letter in value:
            if letter.isalpha():
                self.WordSolver.input(letter=letter, available=False)

        if (
            self.WordSolver.positions == []
            and self.WordSolver.letters == [None for _ in range(self.selected_number)]
            and self.WordSolver.noAvaliable == []
            and self.WordSolver.lettersNoPos == []
            and self.WordSolver.notOnPosition == {}
        ):
            self.word_list.text = ""
        else:
            searchedWords = self.WordSolver.search()
            self.word_list.text = "\n".join(searchedWords)

    def on_word1_delete(self, instance):
        # Here you can add the logic to handle word1 deletion
        self.word_list.text = ""
        self.WordSolver.noAvaliable = []  # Reset the noAvailable letters

        # Re-add all letters that are still in the input
        for letter in instance.text:
            if letter.isalpha():
                self.WordSolver.input(letter=letter, available=False)

        # Update the word list
        if (
            self.WordSolver.positions == []
            and self.WordSolver.letters == [None for _ in range(self.selected_number)]
            and self.WordSolver.noAvaliable == []
            and self.WordSolver.lettersNoPos == []
            and self.WordSolver.notOnPosition == {}
        ):
            self.word_list.text = ""
        else:
            searchedWords = self.WordSolver.search()
            self.word_list.text = "\n".join(searchedWords)

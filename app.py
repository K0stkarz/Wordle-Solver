from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from solver import *

class CustomWordInput(TextInput):
    def __init__(self, app_instance, input_callback, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.input_callback = input_callback
        self.delete_callback = delete_callback
        self.last_text = ''
        self.select_text_on_delete = False

    def insert_text(self, substring, from_undo=False):
        super().insert_text(substring, from_undo=from_undo)
        if self.text != self.last_text:  # Tylko jeśli tekst się zmienił
            self.input_callback(self, self.text)
            self.last_text = self.text

    def do_backspace(self, from_undo=False, mode='bkspc'):
        old_text = self.text
        super().do_backspace(from_undo, mode)
        
        # Sprawdzamy czy tekst został całkowicie usunięty (np. przez Ctrl+A + Backspace)
        if old_text and not self.text:
            self.delete_callback(self)
        # Sprawdzamy czy tekst się zmienił i czy nie jest to usuwanie zaznaczonego tekstu
        elif old_text != self.text and not self.selection_text:
            self.delete_callback(self)
        
        self.last_text = self.text

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # Obsługa Ctrl+A
        if keycode[1] == 'a' and 'ctrl' in modifiers:
            self.select_all()
            return True
            
        # Obsługa Delete gdy tekst jest zaznaczony
        if keycode[1] in ('delete', 'backspace') and self.selection_text == self.text:
            old_text = self.text
            self.text = ''
            if old_text != self.text:
                self.delete_callback(self)
            return True
            
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

class LimitedTextInput(TextInput):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance

    def insert_text(self, substring, from_undo=False):
        if len(self.text) < 1 and substring.isalpha():
            super().insert_text(substring, from_undo=from_undo)
            self.app_instance.on_letter_input(self)
            next_index = self.index + 1
            if next_index < len(self.app_instance.letter_inputs):
                self.app_instance.letter_inputs[next_index].focus = True

    def do_backspace(self, from_undo=False, mode='bkspc'):
        old_text = self.text
        super().do_backspace(from_undo, mode)
        
        # Sprawdzamy czy tekst został usunięty
        if old_text and not self.text:
            self.app_instance.on_letter_delete(self)
            prev_index = self.index - 1
            if prev_index >= 0:
                self.app_instance.letter_inputs[prev_index].focus = True

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # Obsługa Ctrl+A
        if keycode[1] == 'a' and 'ctrl' in modifiers:
            self.select_all()
            return True
            
        # Obsługa Delete/Backspace gdy tekst jest zaznaczony
        if keycode[1] in ('delete', 'backspace') and self.selection_text == self.text:
            old_text = self.text
            self.text = ''
            if old_text:
                self.app_instance.on_letter_delete(self)
                prev_index = self.index - 1
                if prev_index >= 0:
                    self.app_instance.letter_inputs[prev_index].focus = True
            return True

        # Obsługa Tab
        if keycode[1] == 'tab':
            next_index = self.index + 1
            if next_index < len(self.app_instance.letter_inputs):
                self.app_instance.letter_inputs[next_index].focus = True
            return True
            
        return super().keyboard_on_key_down(window, keycode, text, modifiers)
    
class LimitedTextInputNotOnPosition(TextInput):
    def __init__(self, app_instance, max_length,**kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.max_length = max_length

    def insert_text(self, substring, from_undo=False):
        if len(self.text) + len(substring) > self.max_length:
            substring = substring[:self.max_length - len(self.text)]
        if len(self.text) < self.max_length and substring.isalpha():
            super().insert_text(substring, from_undo=from_undo)
            self.app_instance.on_letter_input_not_on_pos(self, to_add=substring)
            # next_index = self.index + 1
            # if next_index < len(self.app_instance.letter_inputs):
            #     self.app_instance.letter_inputs[next_index].focus = True

    def do_backspace(self, from_undo=False, mode='bkspc'):       
        old_text = self.text[len(self.text)-1]
        super().do_backspace(from_undo, mode)
        
        self.app_instance.on_letter_delete_not_on_pos(self, to_del = old_text)
        # prev_index = self.index - 1
        # if prev_index >= 0:
        #     self.app_instance.letter_inputs[prev_index].focus = True

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # Obsługa Ctrl+A
        if keycode[1] == 'a' and 'ctrl' in modifiers:
            self.select_all()
            return True
            
        # Obsługa Delete/Backspace gdy tekst jest zaznaczony
        if keycode[1] in ('delete', 'backspace') and self.selection_text == self.text:
            old_text = self.text
            self.text = ''
            if old_text:
                self.app_instance.on_letter_delete(self)
                # prev_index = self.index - 1
                # if prev_index >= 0:
                #     self.app_instance.letter_inputs[prev_index].focus = True
            return True

        # Obsługa Tab
        if keycode[1] == 'tab':
            # next_index = self.index + 1
            # if next_index < len(self.app_instance.letter_inputs):
            #     self.app_instance.letter_inputs[next_index].focus = True
            return True
            
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.WordSolver = None  # Inicjalizacja WordSolver jako None
        
    def build(self):
        self.title = "Wordle Solver"  # Set the window title
        
        root_layout = BoxLayout(orientation='vertical', padding=10)

        top_layout = BoxLayout(orientation='vertical', padding=10, spacing=5, size_hint_y=None)
        top_layout.bind(minimum_height= top_layout.setter('height'))
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=44)
        
        self.clear_button = Button(
            text="Wyczyść",
            size_hint=(None, None),
            size=(100, 44),
            on_press=self.clear_all_inputs
        )
        button_layout.add_widget(self.clear_button)

        self.spinner_layout = AnchorLayout(anchor_x='right', anchor_y='top')
        self.spinner = Spinner(
            text='Wybierz liczbę',
            values=[str(i) for i in range(3, 11)],
            size_hint=(None, None),
            size=(100, 44)
        )
        self.spinner.bind(text=self.on_spinner_select)
        self.spinner_layout.add_widget(self.spinner)
        button_layout.add_widget(self.spinner_layout)
        
        top_layout.add_widget(button_layout)

        top_layout.add_widget(self.create_label_input('Litery których nie ma w słowie'))
        self.word1 = CustomWordInput(
            app_instance=self,
            input_callback=self.on_word1_input,
            delete_callback=self.on_word1_delete,
            hint_text='Wpisz Litery',
            multiline=False,
            size_hint_y=None,
            height=30
        )
        top_layout.add_widget(self.word1)

        self.letters_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.letters_layout.bind(minimum_height=self.letters_layout.setter('height'))
        self.letters_layout.size_hint_y = None
        self.letters_layout.height = self.letters_layout.minimum_height
        top_layout.add_widget(self.letters_layout)

        root_layout.add_widget(top_layout)

        self.word_list = TextInput(hint_text='Wyświetlane słowa', multiline=True, readonly=True, size_hint=(0.9, 0.5))
        
        bottom_layout = BoxLayout(size_hint_y=0.5, padding=[10, 0])
        bottom_layout.add_widget(self.word_list)
        
        root_layout.add_widget(bottom_layout)

        return root_layout

    def create_label_input(self, text):
        box = BoxLayout(orientation='vertical', size_hint_y=None, height=50)
        label = Label(text=text, size_hint_y=None, height=20, halign='left', valign='middle')
        label.bind(size=label.setter('text_size'))
        box.add_widget(label)
        return box

    def on_spinner_select(self, spinner, text):
        self.word_list.text = ""
        # Tworzenie obiektu po wyborze liczby
        self.selected_number = int(text)
        
        self.WordSolver = Word(self.selected_number)

        # Usuń istniejące pola tekstowe
        self.letters_layout.clear_widgets()
        
        # Lista referencji do pól tekstowych
        self.letter_inputs = []

        # Dodaj nowe pola tekstowe w zależności od wybranej liczby
        num_fields = self.selected_number
        self.letters_layout.cols = num_fields
        self.letters_layout.size_hint_y = None
        self.letters_layout.height = 60 # Zwiększona wysokość dla numeracji

        for i in range(1, num_fields + 1):
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=60)
            letter_input = LimitedTextInput(app_instance=self, hint_text='Wpisz literę', multiline=False, size_hint_y=None, height=30)
            letter_input.index = i - 1  # Dodanie indeksu do pola tekstowego
            number_label = Label(text=str(i), size_hint_y=None, height=20, halign='center', valign='middle')
            number_label.bind(size=number_label.setter('text_size'))
            box.add_widget(letter_input)
            box.add_widget(number_label)
            self.letters_layout.add_widget(box)
            
            # Dodaj pole tekstowe do listy referencji
            self.letter_inputs.append(letter_input)
        
        
            
        for i in range(1, num_fields + 1):
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=60)
            letter_input = LimitedTextInputNotOnPosition(app_instance=self, max_length=self.selected_number ,hint_text='Wpisz literę', multiline=False, size_hint_y=None, height=30)
            letter_input.index = i - 1  # Dodanie indeksu do pola tekstowego
            number_label = Label(text=str(i), size_hint_y=None, height=20, halign='center', valign='middle')
            number_label.bind(size=number_label.setter('text_size'))
            box.add_widget(letter_input)
            box.add_widget(number_label)
            self.letters_layout.add_widget(box)
            
            # Dodaj pole tekstowe do listy referencji
            self.letter_inputs.append(letter_input)
    
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
        if hasattr(self, 'letter_inputs'):
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
        if self.WordSolver.positions == [] and self.WordSolver.letters == [None for _ in range(self.selected_number)] and self.WordSolver.noAvaliable == [] and self.WordSolver.lettersNoPos == [] and self.WordSolver.notOnPosition == {}:
            self.word_list.text = ""
        else:
            searchedWords = self.WordSolver.search()
            self.word_list.text = "\n".join(searchedWords)
            
    def on_letter_input_not_on_pos(self, text_input, to_add):
        # Funkcja wywoływana po wpisaniu litery
        self.word_list.text = ""
        position = text_input.index

        # Wywołanie metody WordSolver.input z literą i pozycją
        self.WordSolver.input(to_add, notOnPosition=position)
        
        # Aktualizacja pola wyświetlania słów
        searchedWords = self.WordSolver.search()
        self.word_list.text = "\n".join(searchedWords)

    def on_letter_delete_not_on_pos(self, text_input, to_del):
        # Funkcja wywoływana po skasowaniu litery
        
        self.word_list.text = ""
        
        self.WordSolver.undo(to_del, notOnPosition=text_input.index)

        # Aktualizacja pola wyświetlania słów
        if self.WordSolver.positions == [] and self.WordSolver.letters == [None for _ in range(self.selected_number)] and self.WordSolver.noAvaliable == [] and self.WordSolver.lettersNoPos == [] and self.WordSolver.notOnPosition == {}:
            self.word_list.text = ""
        else:
            searchedWords = self.WordSolver.search()
            self.word_list.text = "\n".join(searchedWords)

    def on_word1_input(self, instance, value):
        
        self.word_list.text = ""
        
        for letter in value:
            if letter.isalpha():
                self.WordSolver.input(letter=letter, available=False)
                
        if self.WordSolver.positions == [] and self.WordSolver.letters == [None for _ in range(self.selected_number)] and self.WordSolver.noAvaliable == [] and self.WordSolver.lettersNoPos == [] and self.WordSolver.notOnPosition == {}:
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
        if self.WordSolver.positions == [] and self.WordSolver.letters == [None for _ in range(self.selected_number)] and self.WordSolver.noAvaliable == [] and self.WordSolver.lettersNoPos == [] and self.WordSolver.notOnPosition == {}:
            self.word_list.text = ""
        else:
            searchedWords = self.WordSolver.search()
            self.word_list.text = "\n".join(searchedWords)

if __name__ == "__main__":
    MyApp().run()
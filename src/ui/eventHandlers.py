from . import BoxLayout, WordFinder, LimitedTextInput, Label, LimitedTextInputNotOnPosition

class EventHandlers:
    def __init__(self, word_solver: WordFinder, word_list, letters_layout, in_letters_layout, selected_number, words, word1, word1_box, correct_letters_box, incorrect_letters_box):
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
        # Show word1_box
        self.word1_box.opacity = 1
        self.word1_box.disabled = False

        # Show word1_box
        self.correct_letters_box.opacity = 1
        self.correct_letters_box.disabled = False

        # Show word1_box
        self.incorrect_letters_box.opacity = 1
        self.incorrect_letters_box.disabled = False
        

        self.word_list.text = ""
        # Tworzenie obiektu po wyborze liczby
        self.selected_number = int(text)
        
        self.WordSolver = WordFinder(self.selected_number, self.words)

        # Usuń istniejące pola tekstowe
        self.letters_layout.clear_widgets()
        self.in_letters_layout.clear_widgets()

        # Lista referencji do pól tekstowych
        self.letter_inputs = []

        # Dodaj nowe pola tekstowe w zależności od wybranej liczby
        num_fields = self.selected_number
        self.letters_layout.cols = num_fields
        self.letters_layout.size_hint_y = None
        self.letters_layout.height = 60 # Zwiększona wysokość dla numeracji

        self.in_letters_layout.cols = num_fields
        self.in_letters_layout.size_hint_y = None
        self.in_letters_layout.height = 60 # Zwiększona wysokość dla numeracji

        

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
            letter_input.index = i - 1 + num_fields  # Dodanie indeksu do pola tekstowego
            number_label = Label(text=str(i), size_hint_y=None, height=20, halign='center', valign='middle')
            number_label.bind(size=number_label.setter('text_size'))
            box.add_widget(letter_input)
            box.add_widget(number_label)
            self.in_letters_layout.add_widget(box)
            
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
        self.WordSolver.input(to_add, notOnPosition=position - self.selected_number)
        
        # Aktualizacja pola wyświetlania słów
        searchedWords = self.WordSolver.search()
        self.word_list.text = "\n".join(searchedWords)

    def on_letter_delete_not_on_pos(self, text_input, to_del):
        # Funkcja wywoływana po skasowaniu litery
        
        self.word_list.text = ""
        
        self.WordSolver.undo(to_del, notOnPosition=text_input.index - self.selected_number)

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
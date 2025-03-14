class WordFinder:
    def __init__(self, length, words):
        self.length = length
        self.letters = [None for _ in range(length)]
        self.lettersNoPos = []
        self.results = []
        self.positions = []
        self.noAvaliable = []
        self.notOnPosition = {}
        self.words = [word.strip() for word in words if len(word.strip()) == length]

    def __str__(self):
        return "".join(
            [letter if letter is not None else "_" for letter in self.letters]
        )

    def input(self, letter, position=None, available=True, notOnPosition=None):
        if position is not None:
            self.positions.append(position)
            if position >= self.length:
                raise ValueError("Position out of range")
            self.letters[position] = letter.lower()
        elif not available:
            self.noAvaliable.append(letter.lower())
        else:
            if letter.lower() not in self.lettersNoPos:
                self.lettersNoPos.append(letter.lower())
            if letter.lower() not in self.notOnPosition:
                self.notOnPosition[letter.lower()] = []
            self.notOnPosition[letter.lower()].append(notOnPosition)

    def undo(self, letter=None, position=None, available=True, notOnPosition=None):
        if position is not None:
            self.positions.remove(position)
            self.letters[position] = None
        elif not available:
            self.noAvaliable.remove(letter)
        else:
            self.notOnPosition[letter].remove(notOnPosition)
            if self.notOnPosition[letter] == []:
                del self.notOnPosition[letter]
                self.lettersNoPos.remove(letter)

    def search(self):
        self.match_word(self.words)

        return self.results

    def match_word(self, words):
        valid_words = []
        letters_no_pos_set = set(self.lettersNoPos)

        # First filter: Check if letters are in correct positions
        valid_words = [
            word
            for word in words
            if all(word[i] == self.letters[i] for i in self.positions)
        ]

        # Second filter: Check for letters that must be in the word (but not in specific positions)
        if self.lettersNoPos:
            valid_words = [
                word
                for word in valid_words
                if letters_no_pos_set.issubset(
                    self.remove_positions(word, self.positions)
                )
            ]

        # Third filter: Check for letters that must not be in specific positions
        if self.notOnPosition:
            for letter, positions in self.notOnPosition.items():
                valid_words = [
                    word
                    for word in valid_words
                    if all(word[pos] != letter for pos in positions)
                ]

        # Fourth filter: Check for letters that should not be in the word
        # Exclude positions where letters are explicitly placed
        if self.noAvaliable:
            valid_words = [
                word
                for word in valid_words
                if all(
                    letter
                    not in self.remove_positions(
                        word, [i for i, l in enumerate(self.letters) if l == letter]
                    )
                    for letter in self.noAvaliable
                )
            ]

        self.results = valid_words

    def remove_positions(self, word, positions):
        return "".join([char for idx, char in enumerate(word) if idx not in positions])

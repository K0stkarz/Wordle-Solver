from words import *

class Word:
    def __init__(self, length = 5):
        self.length = length
        self.letters = [None for _ in range(length)]
        self.lettersNoPos = []
        self.results = []
        self.positions = []

    def __str__(self):
        return ''.join([letter if letter is not None else '_' for letter in self.letters])

    def input( self, letter, position = None):
        if position is not None:
            self.positions.append(position)
            if position >= self.length:
                print( 'Position out of range' )
                return
            self.letters[position] = letter
        else:
            self.lettersNoPos.append(letter)   
        
        # self.search()
        
    def search( self ):
        if self.letters[0] != None:
            match(self.letters[0]):
                case 'a':         
                    self.match_word(awords)  
                case 'b':
                    self.match_word(bwords)
                case 'k':
                    self.match_word(kwords)
                case _:
                    print('Unknown letter')
        else:
            self.match_word(allwords)

        return self.results

    def match_word( self, words ):
        for word in words:
            a = 0
            for i in self.positions:
                if word[i] == self.letters[i]:
                    a += 1
            if a == len(self.positions):
                self.results.append(word)
            
        
        if self.lettersNoPos != []:
            for word in self.results[:]:
                cutted = self.remove_positions(word, self.positions)

                for letter in self.lettersNoPos:
                    if letter not in cutted and word in self.results:
                        self.results.remove(word)

    def remove_positions(self, word, positions):
        return ''.join([char for idx, char in enumerate(word) if idx not in positions])
    

a = Word()

a.input('k', 0)
a.input('a')

print(a.search())
from words import *

class Word:
    def __init__(self, length = 5):
        self.length = length
        self.letters = [None for _ in range(length)]
        self.lettersNoPos = []
        self.results = []
        self.positions = []
        self.noAvaliable = []
        self.notOnPosition = {}

    def __str__(self):
        return ''.join([letter if letter is not None else '_' for letter in self.letters])

    def input( self, letter, position = None, available = True, notOnPosition = [] ):
        if position is not None:
            self.positions.append(position)
            if position >= self.length:
                print( 'Position out of range' )
                return
            self.letters[position] = letter
        elif not available:
            self.noAvaliable.append(letter)
        else:
            self.lettersNoPos.append(letter)
            self.notOnPosition[letter] = notOnPosition   
        
        # self.search()
        
    def search( self ):
        if self.letters[0] != None:
            match(self.letters[0]):
                case 'a':         
                    self.match_word(awords)  
                case 'ą':
                    self.match_word(ąwords)
                case 'b':
                    self.match_word(bwords)
                case 'c':
                    self.match_word(cwords)
                case 'ć':
                    self.match_word(ćwords)
                case 'd':
                    self.match_word(dwords)
                case 'e':
                    self.match_word(ewords)
                case 'ę':
                    self.match_word(ęwords)
                case 'f':
                    self.match_word(fwords)
                case 'g':
                    self.match_word(gwords)
                case 'h':
                    self.match_word(hwords)
                case 'i':
                    self.match_word(iwords)
                case 'j':
                    self.match_word(jwords)
                case 'k':
                    self.match_word(kwords)
                case 'l':
                    self.match_word(lwords)
                case 'ł':
                    self.match_word(łwords)
                case 'm':
                    self.match_word(mwords)
                case 'n':
                    self.match_word(nwords)
                case 'ń':
                    self.match_word(ńwords)
                case 'o':
                    self.match_word(owords)
                case 'ó':
                    self.match_word(ówords)
                case 'p':
                    self.match_word(pwords)
                case 'q':
                    self.match_word(qwords)
                case 'r':
                    self.match_word(rwords)
                case 's':
                    self.match_word(swords)
                case 'ś':
                    self.match_word(śwords)
                case 't':
                    self.match_word(twords)
                case 'u':
                    self.match_word(uwords)
                case 'v':
                    self.match_word(vwords)
                case 'w':
                    self.match_word(wwords)
                case 'x':
                    self.match_word(xwords)
                case 'y':
                    self.match_word(ywords)
                case 'z':
                    self.match_word(zwords)
                case 'ź':
                    self.match_word(źwords)
                case 'ż':
                    self.match_word(żwords)
                case _:
                    print('Unknown letter')
        else:
            self.match_word(allwords)

        return self.results

    def match_word( self, words ):
        valid_words = []
        letters_no_pos_set = set(self.lettersNoPos)
        no_available_set = set(self.noAvaliable)
        
        for word in words:
            if all(word[i] == self.letters[i] for i in self.positions):
                valid_words.append(word)
        
        if self.lettersNoPos:
            valid_words = [word for word in valid_words if letters_no_pos_set.issubset(self.remove_positions(word, self.positions))]
        
        if self.notOnPosition:
            for letter, positions in self.notOnPosition.items():
                valid_words = [word for word in valid_words if all(word[pos] != letter for pos in positions)]
        
        if self.noAvaliable:
            valid_words = [word for word in valid_words if all(word.count(letter) == 1 for letter in letters_no_pos_set) and all(word.count(letter) <= 1 for letter in no_available_set) and all(word.count(letter) <= 1 for letter in self.noAvaliable)]
        
        self.results = valid_words

    def remove_positions(self, word, positions):
        return ''.join([char for idx, char in enumerate(word) if idx not in positions])
    

a = Word()

a.input('i', notOnPosition=[3])
a.input('b', notOnPosition=[2,3])
a.input('r', 4)
a.input('z')



print(a.search())
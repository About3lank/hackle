import json

class Hackle:
    def __init__(self):
        self.remaining = self.buildDict()
        # self.green = "_____"
        # self.yellow = "_____"
        # self.eliminated = ""

    def run(self):
        self.printHeader()
        won = False
        while not won:
            self.playTurn()
            input("\n   ` Continue? (Press enter) .......")
    
    def buildDict(self):
        remaining = []
        data = {}
        with open('dictionary.json', 'r+') as f:
            data = json.load(f)
        for word in data:
            if len(word)==5 and word.isalpha():
                remaining.append(word)
        return remaining
            
    def sortRemaining(self, remaining):
        alph = "abcdefghijklmnopqrstuvwxyz"
        freq = {}
        scores = {}
        for a in alph:
            freq[a] = [0,0,0,0,0]
        # within remaining words, what is the frequency of each character at each index 0-4
        for word in remaining:
            for i in range(5):
                # print("word/i/word[i] = ", word, "/", i, "/", word[i])
                c = word[i]
                freq[c][i] += 1
        # for each word, how many green letters could potentially be revealed?
        for word in remaining:
            # print("word = ", word)
            score = 0
            for i, c in enumerate(word):
                # print("letter/i/freq_of_letter = ", c, "/", i, "/", freq[c][i])
                score += freq[c][i]
            scores[word] = score

        def findScore(word):
            # print("word/score = ", word, "/", scores[word])
            return scores[word]
        remaining = sorted(remaining, key=findScore, reverse=True)
        return remaining

    def getRemaining(self, green, yellow, elim):
        remaining = []
        # validate each word
        for word in self.remaining:
            valid = True
            for i, c in enumerate(word):
                g = green[i]
                y = yellow[i]
                # eliminated letters
                if c in elim:
                    valid = False
                    break
                # match green
                if g.isalpha() and g!=c:
                    valid = False
                    break
                # yellow check 1
                elif c==y:
                    valid = False
                    break
            # yellow check 2
            for h in yellow:
                if h.isalpha() and h not in word:
                    valid = False
                    break
            # append valid words to updated list
            if valid:
                remaining.append(word)
        return remaining
    
    def playTurn(self):
        print("\n   ` Guess a word, then ....")
        green = input("      ` What's revealed? (Green letters) ..... ").lower()
        yellow = input("      ` What's revealed? (Yellow letters) .... ").lower()
        elim = input("      ` What's eliminated? (Grey letters) .... ").lower()
        for c in elim:
            elim = elim.replace(c, '') if c in green else elim
               
        green = green if green else "-----"
        yellow = yellow if yellow else "-----"
        elim = elim if elim else ""
        self.updateRemaining(green, yellow, elim)
        self.printRemaining()
    
    # def ifIGuess(self, guess, remaining):
    #     # return length of resulting hypothetical possibilities
    #     return 100

    def updateRemaining(self, green, yellow, elim):
        updated = self.getRemaining(green, yellow, elim)
        updated = self.sortRemaining(updated)
        self.remaining = updated

    def isValid(self, guess):
        is_valid = True
        if len(guess)!=5:
            return False, "Guess must be 5 letters. "
        elif not guess.isalpha():
            return False, "Guess must be 5 letters. "
        else:
            for c in guess:
                if c in self.eliminated:
                    return False, "Letter " + c + " has already been eliminated"

        return is_valid, ""

    def printHeader(self):
        print("\n"*4)
        print("   ~~~~~~~~~~~~~~~~~~~~~~ hackle ~~~~~~~~~~~~~~~~~~~~~~   ")
        print("   `````````````` wordle guess generator ``````````````  ") 

    def printRemaining(self):
        print("")
        print("                            ||")
        print("                           _||_")
        print("                           \  /")
        print("                            \/")
        print("")
        print("      ` Remaining possibilities: ")
        for word in self.remaining:
            print("         ` " + word)

h = Hackle()
h.run()
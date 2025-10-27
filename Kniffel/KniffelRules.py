# Rule
import re
RE_Number = r"{0}+?"
RE_Multiple = r"([1-6])\1{0}"
RE_FullHouse = r"([1-6])\1(?!\1)([1-6])\2{2}|([1-6])\3{2}(?!\3)([1-6])\4"
RE_SmallStreet = r"1234|2345|3456"
RE_GreatStreet = r"12345|23456"
RE_Kniffel = r"([1-6])\1{4}"

class Rule:
    def __init__(self, requirement, score):
        self.require = requirement
        self.score = score
        self.amount = 0

    def isMatching(self, diceString):
        found = re.findall(self.require, diceString)
        self.amount = len(found)
        return self.amount > 0
        
    def calculateScore(self):
        return self.score * self.amount

class FoundMultipleRule(Rule):
    def __init__(self, requirement, score):
        Rule.__init__(self, requirement, score)
        self.diceString = ""
        
    def isMatching(self, diceString):
        self.diceString = diceString
        return Rule.isMatching(self, diceString)
    
    def calculateScore(self):
        if self.amount:
            return sum( int(x) for x in self.diceString)
        return 0

class StreetRule(Rule):
    def __init__(self, requirement, score):
        Rule.__init__(self, requirement, score)
        
    def isMatching(self, diceString):
        temp = re.sub(r'(\d)\1+', r'\1', diceString)
        return Rule.isMatching(self, temp)
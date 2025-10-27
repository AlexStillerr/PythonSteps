#---------------------------------------------
# Dateiname: KniffelTest.py
# Do some test
# Autor: Alex Stiller
# Letzte Änderung: 16.09.2025
#---------------------------------------------

from KniffelGameLogic import *

def testScore():
    kniffel = Kniffel()
    kniffel.roll()
    kniffel.checkRules()
    kniffel.debugPrintDice()
    print(kniffel.getResultOfRule(0))
    kniffel.addToScore(0)
    print("----- score added -----")
    for _ in range(5):
        kniffel.roll()
        kniffel.checkRules()
        kniffel.debugPrintDice()
        print(kniffel.getResultOfRule(0))    

def testScoring():
    kniffel = Kniffel()
    
    for i in range(6):
        kniffel.roll()
        kniffel.checkRules()
        kniffel.debugPrintDice()
        print(kniffel.getResultOfRule(i)) 
        kniffel.addToScore(i)
    print(kniffel.getTopScore())

def testRules():
    rule = Rule(RE_Number.format("2"), 2)
    diceString = "12233"
    if rule.isMatching(diceString):
        print(rule.calculateScore())
        
    # 3er pasch
    rule = FoundMultipleRule(RE_Multiple.format("{2}"),0)
    if rule.isMatching(diceString):
        print("3er: not ok")
    diceString = "11333"
    if rule.isMatching(diceString):
        print(rule.calculateScore())
    diceString = "13333"
    if rule.isMatching(diceString):
        print(rule.calculateScore())
    # 4er pasch
    rule = FoundMultipleRule(RE_Multiple.format("{3}"),0)
    if rule.isMatching(diceString):
        print(rule.calculateScore())
      
    # Full house
    rule = Rule(RE_FullHouse, 25)
    diceString = "11233"
    if rule.isMatching(diceString):
        print("FH 1: not ok")
        
    diceString = "11333"
    if rule.isMatching(diceString):
        print(rule.calculateScore())
    else:
        print("FH 2: not ok")
        
    diceString = "11155"
    if rule.isMatching(diceString):
        print(rule.calculateScore())
    else:
        print("FH 3: not ok")
        
    diceString = "55555"
    if rule.isMatching(diceString):
        print("FH 4: not ok")
        
    diceString = "22445"
    if rule.isMatching(diceString):
        print("FH 5: not ok")
        
    # kl Strasse
    rule = StreetRule(RE_SmallStreet, 30)
    diceString = "11235"
    if rule.isMatching(diceString):
        print("kl Str: not ok")
    diceString = "23445"
    if rule.isMatching(diceString):
        print(rule.calculateScore())
    diceString = "23456"
    if rule.isMatching(diceString):
        print(rule.calculateScore())
    
    # gr Strasse
    rule = StreetRule(RE_GreatStreet, 40)
    if rule.isMatching(diceString):
        print(rule.calculateScore())
    diceString = "12346"
    if rule.isMatching(diceString):
        print("gr Str: not ok")
        
    # kniffel
    rule = Rule(r"([1-6])\1{4}", 50)
    diceString = "11233"
    if rule.isMatching(diceString):
        print("kniffel: not ok")
    diceString = "33333"
    if rule.isMatching(diceString):
        print(rule.calculateScore())
    # chance
    rule = FoundMultipleRule(r".", 0)
    diceString = "11233"
    if rule.isMatching(diceString):
        print(rule.calculateScore())
    
if __name__ == "__main__":
    # numbers
    testScoring()

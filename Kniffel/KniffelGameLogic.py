#---------------------------------------------
# Dateiname: KniffelGameLogic.py
# Das Würfelspiel Kniffel in digitaler Form. Der Spieler kann bis zu 3 mal würfeln und sich dann
# aussuchen in welchem Feld er das Ergebnis eintragen möchte
# Autor: Alex Stiller
# Letzte Änderung: 16.09.2025
#---------------------------------------------

from random import randint
from enum import IntEnum
from KniffelRules import *

class DiceState(IntEnum):
    Unselected = 0
    Selected = 1
    Inactive = 2
    
class Dice:
    def __init__(self):
        self.value = -1
        self.diceState = DiceState.Inactive
    
    def roll(self):
        self.value = randint(1, 6)
    
    def setBySide(self):
        self.diceState = DiceState.Selected
        
    def setToShaker(self):
        self.diceState = DiceState.Unselected
    
    def setInactive(self):
        self.diceState = DiceState.Inactive
        
    def __lt__(self, other):
        return self.value < other.value

class PlayerState:
    def __init__(self, playerId):
        self.score = []
        self.playerId = playerId
    
    def addScore(self, ruleId, score):
        dic = {"id":ruleId,"score":score}
        self.score.append(dic)
        
    def canScore(self, ruleId):
        entry = list(filter(lambda s : s["id"] == ruleId, self.score))
        return not entry
    
    def getScore(self, ruleId):
        entry = list(filter(lambda s : s["id"] == ruleId, self.score))
        if entry :
            return entry[0]["score"]
        return None
         
    def getTopScore(self):
        top = [x for x in self.score if x["id"] <= 5]
        return sum( x["score"] for x in top)
    
    def getBottomScore(self):
        bottom = [x for x in self.score if x["id"] > 5]
        return sum( x["score"] for x in bottom)
    
    def getBonusScore(self):
        if self.getTopScore() >= Bonus_Border:
            return Bonus_Value
        return 0
    
    def getTotal(self):
        score = self.getTopScore()
        score += self.getBonusScore()
        score += self.getBottomScore()
        return score
    
    def reset(self):
        self.score.clear()

    def scoreCount(self): return len(self.score)
    
MAX_DiceRolls = 3
Bonus_Border = 63
Bonus_Value = 35

class GameState(IntEnum):
    WaitForFirstRoll = 0
    ShuffleDice = 1
    SelectResult = 2

class KniffelGameLogic:
    def __init__(self, playerCount):
        self.dices = [Dice(),Dice(),Dice(),Dice(),Dice()]
        
        self.rules = [Rule(RE_Number.format("1"), 1),
                      Rule(RE_Number.format("2"), 2),
                      Rule(RE_Number.format("3"), 3),
                      Rule(RE_Number.format("4"), 4),
                      Rule(RE_Number.format("5"), 5),
                      Rule(RE_Number.format("6"), 6),
                      FoundMultipleRule(RE_Multiple.format("{2}"),0),
                      FoundMultipleRule(RE_Multiple.format("{3}"),0),
                      Rule(RE_FullHouse,25),
                      StreetRule(RE_SmallStreet, 30),
                      StreetRule(RE_GreatStreet, 40),
                      Rule(RE_Kniffel, 50),
                      FoundMultipleRule(r".",0)# chance
                      ]
        self.rollsLeft = 0
        self.isActiveRound = False
        
        self.currentPlayer = 0
        self.playerCount = playerCount
        self.players = [PlayerState(id) for id in range(playerCount)]
        self.diceString = ""
    
    def _convertToString(self):
        self.dices.sort()
        self.diceString = "".join(str(x.value) for x in self.dices)

    def startShaking(self):
        for d in self.dices:
            if d.diceState == DiceState.Inactive:
                d.setToShaker()
            elif not self.isActiveRound:
                d.setToShaker()
                      
    def roll(self):
        if self.isActiveRound:
            self._rollDices()
        else:
            self._newRound()
            self._rollDices()
            
    def _newRound(self):
        for d in self.dices:
            d.setToShaker()
        self.rollsLeft = MAX_DiceRolls
        self.isActiveRound = True
            
    def _rollDices(self):
        if self.canRollDice():
            self.rollsLeft -= 1
            activeDices = list(filter(lambda d : d.diceState == DiceState.Unselected, self.dices))
            for d in activeDices:
                d.roll()
        self._updateDiceState()
    
    def _updateDiceState(self):
        if self.rollsLeft <= 0:
            [d.setInactive() for d in self.dices]
            
    def checkRules(self):
        self._convertToString()
        for r in self.rules:
            r.isMatching(self.diceString)
    
    '''
    def selectDice(self, diceValue):
        for d in self.dices:
            if d.diceState == DiceState.Unselected and d.value == diceValue:
                d.setBySide()
                return True
        return False'''
    
    def getDiceValueAtPosition(self, pos):
        if self.dices[pos].value == -1:
            return None
        return self.dices[pos].value
    
    def getDiceStateAtPosition(self, pos):
        return self.dices[pos].diceState
    
    def getResultOfRule(self, ruleId, playerId):
        entry = self._getPlayer(playerId).getScore(ruleId)
        if entry :
            return entry
        if self.isActiveRound:
            return self.rules[ruleId].calculateScore()
        return 0
    
    def toggleDiceState(self, diceId):
        if self.dices[diceId].diceState == DiceState.Selected:
            self.dices[diceId].setToShaker()
        elif self.dices[diceId].diceState == DiceState.Unselected:
            self.dices[diceId].setBySide()
    
    def canScore(self, ruleId, playerId = -1):
        if self.isActiveRound:
            return self._getPlayer(playerId).canScore(ruleId)
        return False
    
    def canRollDice(self):
        return self.rollsLeft > 0

    def addToScore(self, ruleId):
        self._getPlayer(self.currentPlayer).addScore(ruleId, self.getResultOfRule(ruleId, self.currentPlayer))
        self.rollsLeft = 0
        self.isActiveRound = False
        self._nextPlayer()
        
    def _nextPlayer(self):
        self.currentPlayer = (self.currentPlayer +1) % self.playerCount
    
    def _getPlayer(self, playerId):
        if playerId == -1:
            playerId = self.currentPlayer
        return self.players[playerId]
    
    def getTopScore(self, playerId = -1):
        return self._getPlayer(playerId).getTopScore()
    
    def getBottomScore(self, playerId = -1):
        return self._getPlayer(playerId).getBottomScore()
    
    def getBonusScore(self, playerId = -1):
        return self._getPlayer(playerId).getBonusScore()
    
    def getTotal(self, playerId = -1):
        return self._getPlayer(playerId).getTotal()

    def debugPrintDice(self):
        for d in self.dices:
            print(d.value, end=" ")
        print()
    
    def save(self):
        pass
    
    def load(self):
        pass
    
    def newGame(self):
        for p in self.players:
            p.reset()
        self.rollsLeft = 0
        self.isActiveRound = False
           
    def isGameOver(self):
        for p in self.players:
            if self._getPlayer(p.playerId).scoreCount() < len(self.rules):
                return False
        return True
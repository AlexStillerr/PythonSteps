from agent import AgentMonteCarlo
from KniffelGameLogic import KniffelGameLogic
import numpy as np

NormalizeScore = [5,10,15,20,25,30,  30,30,25,30,40,25,60] # kniffel and chance need a special value

class AgentKniffel(AgentMonteCarlo):
    def __init__(self, alpha=0.15, randomFactor=0.2):
        super().__init__(alpha, randomFactor)
        self.brain = {} # line from the block, list of dice combinations

    def getNextState(self, state, action):
        return state.addAction(action)
    
    def print(self, diceState, actions):
        print(diceState)
        print(actions)
        for a in actions:
            state = self.getNextState(diceState, a)
            value = self.getValue(state)
            print(f"{a} -> {value}")


class KniffelState:
    def __init__(self, dices, board):
        self.dices = dices
        self.board = board

    def addAction(self, action):
        match action[0]:
            case 'R': 
                return KniffelState(self.dices, self.board)
            case "S":
                ruleId = int(action.replace("S",""))
                newBoard = self.board | (1<<ruleId)
                return KniffelState(self.dices, newBoard)
            case "T":
                diceId = int(action.replace("TD",""))
                newDice = list(self.dices)
                newDice[diceId] -= 1
                return KniffelState(newDice, self.board)
        return KniffelState(self.dices, self.board)

    def __eq__(self, other):
        if not isinstance(other, KniffelState):
            return False
        return( self.dices == other.dices)

    def __hash__(self):
        return hash((tuple(self.dices), self.board))
    
    def __repr__(self):
        return f"{self.dices} - {[self.board&(1<<x) // (1<<x) for x in range(13)]}"
        

# environment
class KniffelBlock:
    def __init__(self, playerCount):
        self.game = KniffelGameLogic(playerCount)
        self.state = []
        self.lastScore = 0
        self.bestScore = 0
        self.round = 0
        self.boardState = [0,0,0]
        self.countWinner = [0,0,0]
        
    def _getDiceState(self):
        state = [0,0,0,0,0,0]
        for i in range(5):
            dv = self.game.dices[i].value -1
            if dv >=0:
                state[dv] += 1
        return state
    
    def getState(self):
        self.state = KniffelState(self._getDiceState(), self.boardState[self.game.currentPlayer])

        return self.state

    def getReward(self):
        if self.isGameOver():
            return self.game.getTotal()
        return self.lastScore
    
    def getActions(self):
        # S = Score, D = select Dice, R = Roll dice
        actions = []
        for i in range(len(self.game.rules)):
            if self.game.canScore(i):
                actions.append(f"S{i}")

        if self.game.canRollDice():
            for i in range(5):
                actions.append(f"TD{i}")
            
        if self.game.canRollDice() or self.game.isActiveRound == False:
            actions.append("R")
        return actions

    def applyAction(self, action:str):
        self.lastScore = 0
        match action[0]:
            case "S":
                ruleId = int(action.replace("S",""))
                self.lastScore = self.game.getResultOfRule(ruleId, self.game.currentPlayer) / NormalizeScore[ruleId]
                self.boardState[self.game.currentPlayer] = self.boardState[self.game.currentPlayer] | (1<<ruleId)
                self.game.addToScore(ruleId)
            case "R":
                self.game.startShaking()
                self.game.roll()
                self.game.checkRules()
            case "T":
                action = action.replace("TD","")
                self.game.toggleDiceState(int(action))

    def isGameOver(self):
        return self.game.isGameOver()
    
    def reset(self):
        self.game.newGame()
        self.boardState = [0,0,0]

    def printResult(self):
        ruleName = ["1er","2er","3er","4er","5er","6er","3er pasch", "4er pasch","Fullhouse", "Kl Str.", "Gr Str.", "Kniffel","Chance"]
        for player in range(self.game.playerCount):
            print(f"------- Player {player} -------")
            for i in range(len(self.game.rules)):
                print(f"{ruleName[i]}: {self.game.getResultOfRule(i, player)}")
    
    def printBestTotal(self, round):
        scores = [(self.game.getTotal(x), x) for x in range(self.game.playerCount)]
        best = max(scores)
        if best[0] > self.bestScore:
            self.bestScore = best[0]
            print(f"R{round}: {best[0]}")
        self.countWinner[best[1]] += 1

    def printBoardState(self, playerId):
        for x in range(13):
            if self.boardState[playerId]&(1<<x) > 0:
                print("1",end="")
            else:
                print("0",end="")
        print()
        #print( [self.boardState[playerId]&(1<<x) / (1<<x) for x in range(13)])


def oneTestRound(playerCount, agents:list[AgentKniffel]):
    game = KniffelBlock(playerCount)
    agent = agents[game.game.currentPlayer]
    while not game.isGameOver():
        possibleAction = game.getActions()
        stateDice = game.getState()
        #if game.game.currentPlayer == 0:
            #agent.print(stateDice, possibleAction)
        action = agent.chooseAction(stateDice, possibleAction)
        #print("---")
        game.printBoardState(game.game.currentPlayer)
        game.applyAction(action)
        agent = agents[game.game.currentPlayer]
    game.printResult()

FILE_NAME = "KniffelAILearned.json"

def learnTheGame():
    playerCount = 3
    agents = [AgentKniffel() for _ in range(playerCount)]
    game = KniffelBlock(playerCount)
    #for a in agents:
     #   a.loadLearned(FILE_NAME)

    for i in range(5000):
        agent = agents[game.game.currentPlayer]
        while not game.isGameOver():
            possibleAction = game.getActions()
            stateDice = game.getState()
            action = agent.chooseAction(stateDice, possibleAction)
            
            game.applyAction(action)
            reward = game.getReward()
            state = stateDice.addAction(action)

            agent.updateStateHistory(state, reward)
            agent = agents[game.game.currentPlayer]

        for a in agents:
            a.learn()
        #game.printResult()
        game.printBestTotal(i)
        game.reset()
      #  if i % 1000 == 0:
       #     agents[0].saveLearned(FILE_NAME)

    print(f"player stats 1:{game.countWinner[0]} --- 2:{game.countWinner[1]} --- 3:{game.countWinner[2]}")
    
    oneTestRound(playerCount, agents)

if __name__ == "__main__":
    learnTheGame()


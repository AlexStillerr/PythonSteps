import numpy as np
import json

class Agent:
    def __init__(self, alpha = 0.15, randomFactor = 0.2):
        self.alpha = alpha # learning rate
        self.randomFactor = randomFactor
        self.brain = {}

    def saveLearned(self, path):
        with open(path, mode="w", encoding="utf8") as file:
            json.dump({str(self.brain)}, file, indent=3)

    def loadLearned(self, path):
        try:
            with open(path) as file:
                self.brain = json.load(file)
        except Exception as e:
            print(e)

class AgentMonteCarlo(Agent):
    def __init__(self, alpha = 0.15, randomFactor = 0.2):
        Agent.__init__(self, alpha, randomFactor)
        self.stateHistory = [((0,0), 0)]
        #self.G = {} # reward table
    
    def updateStateHistory(self, state, reward):
        self.stateHistory.append((state, reward))

    def learn(self): # Monte Carlo Value
        G = 0  # cumulative discounted reward
        a = self.alpha
        gamma = 0.9  # discount factor (wie wichtig zukünftige Belohnungen sind)
        for state, reward in reversed(self.stateHistory):
            G = reward + gamma * G
            self.brain[state] = self.getValue(state) + a * (G - self.getValue(state))
        self.stateHistory = []
        self.randomFactor = max(0.01, self.randomFactor * 0.995)

    def getValue(self, state):
        return self.brain.get(state, 0.0)
    
    def getNextState(self, state, action):
        return None

    def chooseAction(self, state, allowedMoves):
        nextMove = None

        n = np.random.random()
        if n < self.randomFactor:
            nextMove = np.random.choice(allowedMoves)
        else:
            maxG = -10e15 # a really small random number
            for action in allowedMoves:
                newState = self.getNextState(state, action)
                if self.getValue(newState) >= maxG:
                    nextMove = action
                    maxG = self.getValue(newState)

        return nextMove
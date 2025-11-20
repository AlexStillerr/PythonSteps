import numpy as np
import json

class Agent:
    def __init__(self, alpha = 0.15, randomFactor = 0.2):
        self.alpha = alpha # learning rate
        self.randomFactor = randomFactor
        self.brain = {}

    def saveLearned(self, path):
        with open(path, mode="w", encoding="utf8") as file:
            json.dump(self.brain, file, indent=3)

    def loadLearned(self, path):
        try:
            with open(path) as file:
                self.brain = json.load(file)
        except Exception as e:
            print(e)

class AgentMonteCarlo(Agent):
    def __init__(self, alpha = 0.15, randomFactor = 0.2):
        Agent.__init__(self, alpha, randomFactor)
        self.stateHistory = [] # ((0,0), 0)
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
    
    def getRandomAction(self, moves):
        return np.random.choice(moves)

    def chooseLearnAction(self, state, allowedMoves):
        nextMove = None
        n = np.random.random()
        if n < self.randomFactor:
            nextMove = self.getRandomAction(allowedMoves) 
        else:
            nextMove = self.chooseRealAction(state, allowedMoves)    

        return nextMove
    
    def chooseRealAction(self, state, allowedMoves):
        nextMove = None
        maxG = -10e15 # a really small random number
        for action in allowedMoves:
            newState = self.getNextState(state, action)
            if self.getValue(newState) > maxG:
                nextMove = action
                maxG = self.getValue(newState)
        return nextMove


class AgentQLearning(Agent): # work in progress
    def __init__(self, playerId, alpha = 0.15, randomFactor = 0.2):
        self.playerId = playerId
        self.alpha = alpha # learning rate
        self.randomFactor = randomFactor
        #self.Q = {} 
        
    def getValue(self, state, action):
        return self.brain.get((state, action), 0.0)

    def getNextState(self, state, action):
        newState = [s for s in state]
        newState[action] = str(self.playerId)
        newState = "".join(newState)
        return newState

    def chooseAction(self, state, allowedMoves):
        n = np.random.random()
        if n < self.randomFactor and self.isLearning:
            return np.random.choice(allowedMoves)
        
        qValues = [self.getValue(state, action) for action in allowedMoves]
        maxValue = max(qValues)
        bestActions = [a for a in allowedMoves if self.getValue(state, a) == maxValue]
        
        return np.random.choice(bestActions)

    
    # learn on the fly
    def learn(self, state, action, reward):
        # s = state
        # a = action
        # R = Reward
        # g = gamma
        # V = value of a field
        # bellmann
        # V(s) = max(R(s,a) + gV(s'))
        # markov Decision Process (MDP)
        # V(s) = max(R(s,a) + g*(0.8*V(s1')+0.1*V(s2')+ 0.1*V(s3')))
        # V(s) = max(R(s,a) + g* Sum(P(s,a,s')*V(s')))
        #           a               s'
        # deterministic search vs Non-Deteministic Search
        #
        # Q-Learning
        # per action learning
        # Q(s,a) = R(s,a) + g* Sum(P(s,a,s')*V(s'))
        # Q(s,a) = R(s,a) + g* Sum(P(s,a,s')* max Q(s',a'))
        #                        s'             a'
        # Q(s,a) = R(s,a) + g* max Q(s',a')
        # TD(s,a) = R(s,a) + g* max Q(s',a') - Qt-1(s,a)

        # Qt(s,a) = Qt-1(s,a) + alpha* TDt(s,a)
        # Qt(s,a) = Qt-1(s,a) + alpha*( R(s,a) + g* max Q(s',a') - Qt-1(s,a) )
        alpha = self.alpha
        gamma = 0.9
        
        
        maxQ = 1
        td = reward + gamma * maxQ- self.G[state]
        self.G[state] = self.G[state] + alpha * td
        

    def printReward(self):
        nr = str(self.playerId)
        print(f"{self.getValue(f"{nr}00000000"):.2} {self.getValue(f"0{nr}0000000"):.2} {self.getValue(f"00{nr}000000"):.2}")
        print(f"{self.getValue(f"000{nr}00000"):.2} {self.getValue(f"0000{nr}0000"):.2} {self.getValue(f"00000{nr}000"):.2}")
        print(f"{self.getValue(f"000000{nr}00"):.2} {self.getValue(f"0000000{nr}0"):.2} {self.getValue(f"00000000{nr}"):.2}")
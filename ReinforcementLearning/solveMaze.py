from environment import Maze
from agent import AgentMonteCarlo
import numpy as np

ACTIONS = {'U':(-1,0), 'D':(1,0), 'L':(0, -1), 'R':(0, 1)}

class AgentMaze(AgentMonteCarlo):
    def __init__(self, states, alpha = 0.15, randomFactor = 0.2):
        AgentMonteCarlo.__init__(self, alpha, randomFactor)
        self.initReward(states)

    def initReward(self, states):
        for x, row in enumerate(states):
            for y, col in enumerate(row):
                if col == 1:
                    self.brain[(x,y)] = 0.0
                else:
                    self.brain[(x,y)] = np.random.uniform(high=1.0, low=0.1)

    def learn(self):
        AgentMonteCarlo.learn(self)
        # G = reward + gamma * G
        # self.G[state] = self.G[state] + a * (G - self.G[state])
        
        # start state=(5,5)
        # G = 1 + 0.9 * 0                           -> G = 1
        # self.G[state] = 0 + 0.15 * ( 1 - 0)       -> 0.15

        # 1 step state=(4,5)
        # G = -1 + 0.9 * 1                          -> G = -0.1
        # self.G[state] = 0 + 0.15 * ( -0.1 - 0)    -> -0.015
        
        # 2 step state=(4,4)
        # G = -1 + 0.9 * -0.1                       -> G = -1.09
        # self.G[state] = 0 + 0.15 * ( -1.09 - 0)   -> -0.1635
        
        # 3 step state=(4,5)
        # G = -1 + 0.9 * -1.09                      -> G = -1.981
        # self.G[state] = -0.015 + 0.15 *(-1.981 -0.015) -> -0.3144

    def getNextState(self, state, action):
        # chat gpt sagt das diese zeile zwei tuples addiert, bitte prüfen
        return  tuple([sum(x) for x in zip(state, ACTIONS[action])]) # ????
    
    def printReward(self):
        for x in range(6):
            for y in range(6):
                print(f"{self.G[x,y]:.2} ", end= " ")
            print()

def solveAMaze():
    maze = Maze()
    maze.createTestSetup()
    maze.printMap()
    # create all state or...
    agent = AgentMaze(maze.maze, 0.05)
    #agent.printReward()

    for _ in range(2000): #5000
        while maze.isGameOver() == False:
            state, _ = maze.getStateAndReward()
            # select action
            moves = maze.allowedStates[state]
            action = agent.chooseLearnAction(state, moves)
            
            # Update environment
            maze.updateMaze(action)

            # get updated state and reward
            state, reward = maze.getStateAndReward()
            # store new state and reward in memory
            agent.updateStateHistory(state, reward)
        
        # replay memory of previouse episode to update G
        agent.learn()
        #print(f"steps {maze.steps}")
        maze.reset()
        #agent.printReward()

    # show answer
    print(f"S: {maze.robotPosition}")
    while maze.isGameOver() == False:
        state, _ = maze.getStateAndReward()
        # select action
        moves = maze.allowedStates[state]
        action = agent.chooseRealAction(state, moves)
        
        maze.updateMaze(action)
        print(f"{action}: {maze.robotPosition}")

if __name__ == "__main__":
    solveAMaze()
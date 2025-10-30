import numpy as np

# Environment:
# Alles was der Agent nicht kontrollieren kann ist Teil des Environments
ACTIONS = {'U':(-1,0), 'D':(1,0), 'L':(0, -1), 'R':(0, 1)}

class Maze(object):
    def __init__(self):
        self.maze = np.zeros((6,6))
        self.robotPosition = (0,0)
        self.steps = 0
        self.allowedStates = None

    def createTestSetup(self):
        self.maze[0,0] = 2
        self.maze[5,:5] = 1
        self.maze[:4,5] = 1
        self.maze[2,2:] = 1
        self.maze[3,2] = 1
        self.constructAllowedStates()

    # erzeugt eine Map mit allen möglichen Actions pro Position
    def constructAllowedStates(self):
        allowedStates = {}
        for x, row in enumerate(self.maze):
            for y, _ in enumerate(row):
                if self.maze[(x,y)] != 1:
                    allowedStates[(x,y)] = []
                    for action in ACTIONS:
                        if self.isAllowedMove((x,y), action):
                            allowedStates[(x,y)].append(action)

        self.allowedStates = allowedStates

    def isAllowedMove(self, state, action):
        x, y = state
        x += ACTIONS[action][0]
        y += ACTIONS[action][1]

        if x < 0 or x > 5 or y < 0 or y > 5:
            return False
        
        if self.maze[x,y] == 0 or self.maze[x,y] == 2:
            return True
        return False
    
    def updateMaze(self, action):
        x, y = self.robotPosition
        self.maze[x,y] = 0
        x += ACTIONS[action][0]
        y += ACTIONS[action][1]
        self.robotPosition = (x,y)
        self.maze[x,y] = 2
        self.steps += 1

    def reset(self):
        x, y = self.robotPosition
        self.maze[x, y] = 0
        self.robotPosition = (0,0)
        self.maze[0, 0] = 2
        self.steps = 0

    def isGameOver(self):
        return self.robotPosition == (5,5)

    def giveReward(self):
        if self.robotPosition == (5,5):
            return 1
        return -1
    
    def getStateAndReward(self):
        return self.robotPosition, self.giveReward()
    
    def printState(self):
        for x in range(6):
            for y in range(6):
                print(f"{ self.mapValueToField(self.maze[x,y])} ", end= "")
            print()

    def mapValueToField(self, v):
        match int(v):
            case 0:
                return " "
            case 1:
                return "#"
            case 2:
                return "R"
        return v
    
    def printMap(self):
        for x, row in enumerate(self.maze):
            for y, _ in enumerate(row):
                if self.maze[x,y] != 1:
                    print(f"{(x,y)}", end=" ")
                else:
                    print("######", end=" ")
            print()
 
class TicTacToeField:
    def __init__(self):
        self.field = np.zeros((3,3))
        self.winner = 0

    def reset(self):
        self.winner = 0
        self.field = np.zeros((3,3))

    def getActionsOfState(self, state):
        actions = []
        for i in range(9):
            if state[i] == "0":
                actions.append(i)
        return actions
    
    def createState(self):
        state = ""
        for _, row in enumerate(self.field):
            for _, col in enumerate(row):
                state += str(int(col))
        return state

    def takeAction(self, action, player:int):
        x = action // 3
        y = action % 3
        self.field[x,y] = player
        self.evaluate()
    
    def evaluate(self):
        if self.field[0,0] != 0 and self.field[0,0] == self.field[0,1] == self.field[0,2]:
            self.winner = self.field[0,0]
        if self.field[1,0] != 0 and self.field[1,0] == self.field[1,1] == self.field[1,2]:
            self.winner = self.field[1,0]
        if self.field[2,0] != 0 and self.field[2,0] == self.field[2,1] == self.field[2,2]:
            self.winner = self.field[1,0]
        if self.field[0,0] != 0 and self.field[0,0] == self.field[1,0] == self.field[2,0]:
            self.winner = self.field[0,0]
        if self.field[0,1] != 0 and self.field[0,1] == self.field[1,1] == self.field[2,1]:
            self.winner = self.field[0,1]
        if self.field[0,2] != 0 and self.field[0,2] == self.field[1,2] == self.field[2,2]:
            self.winner = self.field[0,2]
        if self.field[0,0] != 0 and self.field[0,0] == self.field[1,1] == self.field[2,2]:
            self.winner = self.field[0,0]
        if self.field[0,2] != 0 and self.field[0,2] == self.field[1,1] == self.field[2,0]:
            self.winner = self.field[0,2]
    
    def isGameOver(self):
        if self.winner != 0:
            return True
        
        for x in range(3):
            for y in range(3):
                if self.field[x,y] == 0:
                    return False
        return True

    def giveReward(self, player):
        if self.winner == 0:
            return 0
        
        if self.winner == player:
            return 6
        return -5
    
    def print(self):
        for _, row in enumerate(self.field):
            for _, col in enumerate(row):
                if col == 1:
                    print(f" X ", end=" ")
                elif col == 2:
                    print(" O ", end=" ")
                else:
                    print(" - ", end=" ")
            print()

from agent import AgentMonteCarlo


class MatchFourAgent(AgentMonteCarlo):
    def __init__(self, playerId, alpha=0.15, randomFactor=0.2):
        super().__init__(alpha, randomFactor)
        self.playerId = playerId

    def getNextState(self, state, action):
        newState = list(state)
        newState[int(action)] = str(self.playerId)
        return "".join(newState)
    

class MachtFourState:
    field: list

class MatchFourGame:
    def __init__(self):
        self.field = []
        self.colHeight = []
        self.currentPlayer = 1
        self.winningPlayer = 0
        for _ in range(7):
            for _ in range (6):
                self.field.append(0)
            self.colHeight.append(0)
        #self.directions = { (0,1), (1,0), (1,1), (1,-1) }

    directions: list = { (0,1), (1,0), (1,1), (1,-1) }

    def reset(self):
        for col in range(7):
            for row in range (6):
                self.field[self.index(col,row)] = 0
            self.colHeight[col] = 0
        self.winningPlayer = 0

    def index(self, col, row): return col + row*7
    
    def stringState(self): return "".join( str(x) for x in self.field)

    def getPossibleActions(self):
        actions = []
        for col in range(7):
            if self.colHeight[col] < 6:
                actions.append( self.index(col, self.colHeight[col]))
        return actions

    def tryToAddStone(self, col):
        if self.canAddStone(col):
            returnValue = (self.colHeight[col], self.currentPlayer)
            
            self.addStone(col, self.currentPlayer)
            self.swapPlayer()

            return returnValue
        return (-1, -1)
    
    def getReward(self):
        r = []
        if self.winningPlayer == 1:
            r.append(10)
        else:
            r.append(0)
        
        if self.winningPlayer == 2:
            r.append(10)
        else:
            r.append(0)
        return r

    def canAddStone(self, col): return self.colHeight[col] < 6
    def swapPlayer(self): 
        if self.currentPlayer == 1: 
            self.currentPlayer = 2 
        else:
            self.currentPlayer = 1

    def addStone(self, col, player):
        self.field[self.index(col,self.colHeight[col]) ] = player
        self.colHeight[col] += 1

    def checkGameOver(self, player):
        containsEmptyField = False
        for col in range(7):
            for row in range(6):
                if self.field[self.index(col,row)] == 0:
                    containsEmptyField = True
                if self.field[self.index(col,row)] != player:
                    continue
                if self.checkDirections(row, col, player):
                    self.winningPlayer = player
                    return True
        return not containsEmptyField

    def checkDirections(self, row, col, player):
        for (x, y) in self.directions:
            count = 1

            for i in range(4):
                newRow = row + i * y
                newCol = col + i * x

                if newRow < 0 or newCol < 0 or newRow > 5 or newCol > 6:
                    continue

                if self.field[self.index(newCol, newRow)] == player:
                    count += 1

            if count == 4:
                return True
        return False



def trainAi():
    playerOne = MatchFourAgent(1)
    playerTwo = MatchFourAgent(2)
    game = MatchFourGame()
    currentPlayer = playerOne

    wins = [0,0,0]
    for i in range(100000):

        while True:
            actions = game.getPossibleActions()
            
            action = currentPlayer.chooseAction(game.stringState(), actions)
            game.addStone(action%7, currentPlayer.playerId)
            game.swapPlayer()

            reward = game.getReward()
            state = game.stringState()

            playerOne.updateStateHistory(state, reward[0])
            playerTwo.updateStateHistory(state, reward[1])

            if game.currentPlayer == 1:
                currentPlayer = playerOne
            else:
                currentPlayer = playerTwo

            if game.checkGameOver(currentPlayer.playerId):
                break
        
        playerOne.learn()
        playerTwo.learn()

        wins[game.winningPlayer] += 1
        game.reset()

    print(wins)


def tt(super = []):
    super.append(2)
    return super

if __name__ == "__main__":
    trainAi()

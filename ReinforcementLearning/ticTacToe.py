from environment import TicTacToeField
from agent import AgentMonteCarlo


class AgentTTT(AgentMonteCarlo):
    def __init__(self, playerId, alpha = 0.15, randomFactor = 0.2):
        AgentMonteCarlo.__init__(self, alpha, randomFactor)
        self.playerId = playerId
        
    def getNextState(self, state, action):
        newState = [s for s in state]
        newState[action] = str(self.playerId)
        newState = "".join(newState)
        return newState
        
    def printReward(self):
        nr = str(self.playerId)
        print(f"{self.getValue(f"{nr}00000000"):.2} {self.getValue(f"0{nr}0000000"):.2} {self.getValue(f"00{nr}000000"):.2}")
        print(f"{self.getValue(f"000{nr}00000"):.2} {self.getValue(f"0000{nr}0000"):.2} {self.getValue(f"00000{nr}000"):.2}")
        print(f"{self.getValue(f"000000{nr}00"):.2} {self.getValue(f"0000000{nr}0"):.2} {self.getValue(f"00000000{nr}"):.2}")


def learnTicTacToe():
    field = TicTacToeField()
    agents = [AgentTTT(1, 0.05, 0.4), AgentTTT(2, 0.05)]

    currentPlayer = 1
    currentAgent = agents[currentPlayer]
    for i in range(100000):
        if i%10000 == 0:
            print(f"Run {i}")

        lastState = None
        lastAgent = None
        lastPlayerId = None
        while not field.isGameOver():
            #if currentPlayer == 1:
             #   currentAgent = agent2
            #else:
             #   currentAgent = agent1
            currentPlayer = (currentPlayer+1)%2
            currentAgent = agents[currentPlayer]

            state = field.createState()
            actions = field.getActionsOfState(state)
            #print(f"{state} -> {actions} -> {currentPlayer}")

            action = currentAgent.chooseLearnAction(state, actions)

            field.takeAction(action, currentPlayer+1)
            
            newState = field.createState()
            
            if lastAgent:
                if field.isGameOver():
                    reward = field.giveReward(currentPlayer+1)
                    currentAgent.updateStateHistory(newState, reward)
                lastAgent.updateStateHistory(lastState, field.giveReward(lastPlayerId+1))
            
            lastAgent = currentAgent
            lastState = newState
            lastPlayerId = currentPlayer
            

        agents[0].learn()
        agents[1].learn()

        #field.print()
        field.reset()

    print("--------------- Player 1 ----------------")
    #agents[0].setToProduction()
    agents[0].printReward()
    print("--------------- Player 2 ----------------")
    #agents[1].setToProduction()
    agents[1].printReward()

    return agents

def playTicTacToe(agents):  
    field = TicTacToeField()
    #player
    currentAgent = agents[0]
    currentPlayer = 1
    while True:
        while not field.isGameOver():
            print("--------------------------")
            if currentPlayer == 1:
                currentPlayer = 2
            else:
                currentPlayer = 1

            field.print()        
            state = field.createState()
            actions = field.getActionsOfState(state)

            if currentPlayer == 1:
                action = currentAgent.chooseRealAction(state, actions)
            else:
                action = int(input())

            field.takeAction(action, currentPlayer)

        print("Game over")
        field.print()
        print("Weiter?")
        field.reset()
        if input() in 'Nn':
            break


if __name__ == "__main__":
    agents = learnTicTacToe()
    agents[0].saveLearned("TicTacToeAgent.json")
    #agent = AgentTTT(1)
    #agent.loadLearned("TicTacToeAgent.json")
    playTicTacToe(agents)
    print("Ende")

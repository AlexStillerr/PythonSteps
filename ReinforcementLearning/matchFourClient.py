from fastapi import FastAPI
from pydantic import BaseModel # convertiert in json
import uvicorn # webserver ohne schnickschnack

from matchFour import MatchFourAgent

app = FastAPI() # benötigt damit python auf http anfragen reagieren kann

class Test(BaseModel):
    text: str  # variablen erzeugen ohne constructor

@app.post("/echo")
def echo(message:Test):
    print("Received:",message.text)
    return {"reply": "Python hat nachricht erhalten"}



class MachFourState(BaseModel):
    player: int
    field: str
    actions: list
    isProduction: bool

@app.post("/getAction")
def getAction(message:MachFourState):
    if message.player == 1:
        if message.isProduction:
            action = agent1.chooseRealAction(message.field, message.actions)
        else:
            action = agent1.chooseLearnAction(message.field, message.actions)
    else:
        if message.isProduction:
            action = agent2.chooseRealAction(message.field, message.actions)
        else:
            action = agent2.chooseLearnAction(message.field, message.actions)
    return {"action": action}

class MatchFourReward(BaseModel):
    player:int
    field:str
    reward:int

@app.post("/updateHistory")
def getAction(message:MatchFourReward):
    if message.player == 1:
        agent1.updateStateHistory(message.field, message.reward)
    else:
        agent2.updateStateHistory(message.field, message.reward)
    return {"reply": "Update done"}

@app.post("/gameOver")
def learn():
    agent1.learn()
    agent2.learn()
    return {"reply": "Learn done"}

class MatchFourSaveLoad(BaseModel):
    pathP1:str
    pathP2:str

@app.post("/save")
def learn(message:MatchFourSaveLoad):
    agent1.saveLearned(message.pathP1)
    agent2.saveLearned(message.pathP2)
    return {"reply": "Save done"}

@app.post("/load")
def learn(message:MatchFourSaveLoad):
    agent1.loadLearned(message.pathP1)
    agent2.loadLearned(message.pathP2)
    return {"reply": "Load done"}



agent1 = MatchFourAgent(1, 0.05, 0.4)
agent2 = MatchFourAgent(2, 0.05, 0.4)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
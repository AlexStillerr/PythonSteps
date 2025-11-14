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

agent1 = MatchFourAgent(1)
agent2 = MatchFourAgent(2)

class MachFourState(BaseModel):
    player: int
    field: str
    actions: list

@app.post("/getAction")
def getAction(message:MachFourState):
    if message.player == 1:
        action = agent1.chooseAction(message.field, message.actions)
    else:
        action = agent2.chooseAction(message.field, message.actions)
    return {"action": action}

class MatchFourReward(BaseModel):
    field:str
    reward:list

@app.post("/updateHistory")
def getAction(message:MatchFourReward):
    agent1.updateStateHistory(message.field, message.reward[0])
    agent2.updateStateHistory(message.field, message.reward[1])
    return {"reply": "Update done"}

@app.post("/gameOver")
def learn():
    agent1.learn()
    agent2.learn()
    return {"reply": "Learn done"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
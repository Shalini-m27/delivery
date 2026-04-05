from fastapi import FastAPI
from pydantic import BaseModel
from delivery_env import AdaptiveDeliveryEnv

app = FastAPI()
env = AdaptiveDeliveryEnv()

class ActionModel(BaseModel):
    action: int

@app.get("/")
def ping_status():
    return {"status": "ok", "message": "MetaLogistics Space Online (200)"}

@app.get("/reset")
@app.post("/reset")
def reset_env():
    state = env.reset()
    return {"status": "success", "state": state.tolist()}

@app.post("/step")
def step_env(body: ActionModel):
    state, reward, done, _ = env.step(body.action)
    return {"state": state.tolist(), "reward": float(reward), "done": done}

@app.get("/state")
def state_env():
    state = env.state()
    return {"state": state.tolist()}

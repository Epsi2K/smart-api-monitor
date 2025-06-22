from fastapi import FastAPI
from pydantic import BaseModel
import redis
import time
import json

app = FastAPI()

# Connect to Redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Define expected JSON input model
class LogData(BaseModel):
    user: str

@app.get("/")
def root():
    return {"message": "Smart API Monitor running!"}

@app.post("/log")
async def log_request(data: LogData):
    timestamp = str(int(time.time()))
    payload = data.dict()
    r.hset("api_traffic", timestamp, json.dumps(payload))
    return {"status": "logged", "timestamp": timestamp}

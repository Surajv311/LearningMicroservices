import json
from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

@app.get("/")
def health_check_root_endpoint():
    return {"Status: main.py root server healthy"}

# To complete Task1
@app.get("/currentStatus")
def health_check_fun():
    return {"Status: main.py app healthy"}

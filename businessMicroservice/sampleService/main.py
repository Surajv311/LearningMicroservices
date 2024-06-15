import json
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Note: Reason why done ~ https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
from database.postgresDbConfig import *
from database.redisDbConfig import *

app = FastAPI()

@app.get("/")
def health_check_root_endpoint():
    return {"Status: main.py root server healthy"}

# To complete Task1
@app.get("/currentStatus")
def health_check_fun():
    return {"Status: main.py app healthy"}

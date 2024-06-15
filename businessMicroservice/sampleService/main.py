import json
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from ...businessMicroservice.database.postgresDbConfig import * # using 3 dots to get values present in a different module - though not using it currently
from ...businessMicroservice.database.redisDbConfig import *


app = FastAPI()

@app.get("/")
def health_check_root_endpoint():
    return {"Status: main.py root server healthy"}

# To complete Task1
@app.get("/currentStatus")
def health_check_fun():
    return {"Status: main.py app healthy"}

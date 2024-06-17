import json
from fastapi import FastAPI
import requests
import asyncio
import time

app = FastAPI()

@app.get("/")
def consumer_service_status(): # for health check
    return {"Status: consumerService app.py root server healthy"}

# To complete Task10
@app.get("/bmservicestatus")
def get_bmservice_server_status_docker():
    url = 'http://businessmicroservice:8900/bmserviceserverstatus'
    response = requests.get(url)
    print(f"Hitting API from consumerMicroservice")
    print(f"Status of fastapi app server in businessMicroservice: {response.status_code}")
    data = json.loads(response.text)
    return data

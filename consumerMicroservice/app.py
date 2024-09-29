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

# To complete Task12
"""
Note that we don't really have to have another API calling the businessService API, its like API on top of API - which is not a good way to engineer things unless a situation provokes, 
rather we should expose and use businessMicroservice API directly... only thing why we are calling it from another microservice (which as you see has already been implemented in Task10 above) 
is just to mimic how a client or consumer would interact - abstracting from core logic service. 
"""
@app.get('/getusers')
def get_users():
    url = 'http://businessmicroservice:8900/users'
    response = requests.get(url)
    print(response.status_code)
    data = json.loads(response.text)
    return data

@app.get('/getuser/{user_id}')
def get_user(user_id:int):
    url = f'http://businessmicroservice:8900/users/{user_id}' # the user_id
    response = requests.get(url)
    print(response.status_code)
    data = json.loads(response.text)
    return data

@app.get('/postusers')
def post_users():
    """
    Understand that in this parent API we are using get call to access response from the API which in turn internally if you see below, is running logic
    to do a POST API call on businessMicroservice API... One could directly access POST call of businessMicroservice as well, as we have already done the necesary port mappings, etc..
    but as discussed, just want to mimic a consumer/client.
    Currently, as you see, everytime we run it, a static data would be inserted in POST call. In real world cases, it does not happen that way.
    """
    url = 'http://businessmicroservice:8900/users'
    data_body = {
    "name": "TestNameJohn",
    "type": "TestTypeABC",
    "phone": 1234500000,
    "address": "Earth"
    }
    # attributes like id, created_at is done by SQLAlchemy library in businessMicroservice
    response = requests.post(url, json=data_body)
    print(response.status_code)
    data = json.loads(response.text)
    return data

@app.get('/putusers/{user_id}')
def put_users(user_id:int):
    url = f'http://businessmicroservice:8900/users/{user_id}'
    data_body = {
    "name": "ChangedNameXYZ",
    "type": "ChangedABC",
    "phone": 999999992,
    "address": "ChangedAddressWorld"
    }
    response = requests.put(url, json=data_body)
    print(response.status_code)
    data = json.loads(response.text)
    return data

@app.get('/deleteusers/{user_id}')
def delete_users(user_id:int):
    url = f'http://businessmicroservice:8900/users/{user_id}'
    response = requests.delete(url)
    print(response.status_code)
    data = json.loads(response.text)
    return data

"""
Similar like above we can built APIs to access Redis CRUD APIs in businessMicroservice
"""

###########################################################################
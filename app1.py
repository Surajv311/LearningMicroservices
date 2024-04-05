from typing import Union
import json
from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()


# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None




import redis

rd = redis.Redis(host="localhost", port=7001, db =0)


@app.get("/")
def read_root():
    return {"App1": "Opened"}

@app.get("/h1")
def read_root():
    url = 'http://127.0.0.1:8001/h2'
    response = requests.get(url)
    print(f"Status of app2 server: {response.status_code}")
    data = json.loads(response.text)
    return data


@app.get("/rl") # redis local 
def read_root():
    # health of redis url, done port mapping
    x = rd.ping()
    
    rd.set('hi', 'bye')
    y = rd.get('hi')
    # y = rd.get('h1234314i')

    if x and y:
        return "working"
    else:
        return "not working"
    











# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}
    
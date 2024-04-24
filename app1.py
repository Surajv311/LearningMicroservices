from typing import Union
import json
from fastapi import FastAPI
import fastapi as _fastapi
from pydantic import BaseModel
import requests
import schemas as _schemas
from typing import TYPE_CHECKING, List
import sqlalchemy.orm as _orm
import services as _services
import pandas as pd
from sqlalchemy import *
from database import DATABASE_URL, engine, SessionLocal, Base
import asyncio

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

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



# @app.post("/psql/create/", response_model=_schemas._PData)
# def create_data(
#     contact: _schemas._createData,
#     db: _orm.Session = _fastapi.Depends(_services.get_db),
# ):
#     return 'hi'

# @app.get("/psql/health") #async
# def root(db: Session = _fastapi.Depends(_services.get_db)):
#     ### INACTIVE ENDPOINT ####
#     print('hi')
#     pass

@app.get("/psql/h")
def get_data():
    db = SessionLocal()
    # user = db.query(User).filter(User.id == user_id).first()
    # stmt = select([tpsqltable.c.name])
    # result = conn.execute(stmt)
    sql = "select * from tpsqltable"
    df = pd.read_sql(sql, con=engine)
    json_data = json.dumps(json.loads(df.to_json(orient="records")))
    db.close()
    return {json_data}

# @app.get("/pl") # posttgres local
# def read_root():
#     # health of postgresql url, done port mapping
#     print('checking postgres health')

########################################################################

@app.get("/redis")  # redis local
async def redisfun():
    x = rd.ping()
    if x is not None:
        return "working"
    else:
        return "not working"
@app.get("/postgres")
async def postgresfun():
    db = SessionLocal()
    sql = "select * from tpsqltable"
    df = pd.read_sql(sql, con=engine)
    json_data = json.dumps(json.loads(df.to_json(orient="records")))
    db.close()
    return {json_data}

@app.get("/hasync")
async def get_status_of_all():
    url1 = 'http://127.0.0.1:8000/postgres'
    url2 = 'http://127.0.0.1:8000/redis'
    # response1 = requests.get(url1)
    # response2 = requests.get(url2)
    # print(f"Pinging both redis and postgres")
    # data1 = str(json.loads(response1.text))
    # data2 = str(json.loads(response2.text))
    # return data1+data2

    results = await asyncio.gather(*[postgresfun(), redisfun()])
    results = str(results)
    return results


########################################################################






# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}
    
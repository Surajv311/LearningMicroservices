import json
from fastapi import FastAPI
import requests
import pandas as pd
from sqlalchemy import *
from database.postgresDbConfig import engine, SessionLocal, postgres_table
from database.redisDbConfig import rd, redis_client
import asyncio

app = FastAPI()
@app.get("/")
def health_check_root_endpoint():
    return {"Status: app.py root server healthy"}
#################################################################################
# To complete Task1
@app.get("/mainappstatus")
def get_other_server_status():
    url = 'http://127.0.0.1:8001/currentStatus' # Note that endpoint is camelCase, same is expected when typing in url/testing via postman
    response = requests.get(url)
    print(f"Status of main app server: {response.status_code}")
    data = json.loads(response.text)
    return data

#################################################################################
# To complete Task2
@app.get("/redisHealth") # Note the endpoint is in camelCase
def redisHealthFun():
    status = rd.ping() # simply pinging the Redis db
    ## Trying to perform a basic set/get operation
    try:
        if status:
            rd.set('key', 'hello world')
            response = rd.get('key')
            if response:
                data = response.decode('utf-8') # decoding byter to string, as Redis returns: b'hello world', when I print
            else:
                data = "No data - Unable to decode data"
            return {
                "Redis status": "Healthy",
                "Sample Data": data
            }
    except Exception as e:
        print(f"Error occurred: {e}")
        msg = str(e)
        return {
            "Redis status": f"ERROR - {msg}"
        }
@app.get("/postgresHealth") # Note the endpoint is in camelCase
def postgresHealthFun():
    db = SessionLocal()
    try:
        sql_query = f"select 1+1" # A simple query to run on postgres; Yes such query runs in postgres - primarily used for health checks
        df = pd.read_sql(sql_query, con=engine)
        status = not df.empty
        if status:
            # if status is fine and we get some data, we further query on a table and get one row from it
            sql = f"select * from {postgres_table} limit 1"
            df = pd.read_sql(sql, con=engine)
            json_data = json.dumps(json.loads(df.to_json(orient="records")))
            return {
                "Postgres status": "Healthy",
                "Sample Data": json_data
            }
    except Exception as e:
        print(f"Error occurred: {e}")
        msg = str(e)
        return {
            "Postgres status": f"ERROR - {msg}"
        }
    finally:
        db.close()
#################################################################################
# To complete Task3
### Async version
@app.get("/asyncrhealth")
async def redis_fun_async():
    "To get redis db health in async fashion"
    status = rd.ping()
    if status:
        return {"Redis status: Healthy"}
    else:
        return {"Redis status: ERROR; Not working"}
@app.get("/asyncphealth")
async def postgres_fun_async():
    "To get postgres db health in async fashion"
    db = SessionLocal()
    sql_query = f"select 1+1"
    df = pd.read_sql(sql_query, con=engine)
    status = not df.empty
    db.close()
    if status:
        return {"Postgres status: Healthy"}
    else:
        return {"Postgres status: ERROR; Not working"}
@app.get("/asyncrpstatus")
async def get_async_status_db():
    results = await asyncio.gather(*[postgres_fun_async(), redis_fun_async()])
    results = "Async status of both dbs: " + str(results)
    return results
### Sync version - We basically remove async keyword from all, else they exhibit strange behaviour
@app.get("/syncrhealth")
def redis_fun_sync():
    "To get redis db health in sync fashion"
    status = rd.ping()
    if status:
        return {"Redis status: Healthy"}
    else:
        return {"Redis status: ERROR; Not working"}
@app.get("/syncphealth")
def postgres_fun_sync():
    "To get postgres db health in sync fashion"
    db = SessionLocal()
    sql_query = f"select 1+1"
    df = pd.read_sql(sql_query, con=engine)
    status = not df.empty
    db.close()
    if status:
        return {"Postgres status: Healthy"}
    else:
        return {"Postgres status: ERROR; Not working"}
@app.get("/syncrpstatus")
def get_sync_status_db():
    print(f"Pinging both redis and postgres")
    pg_url = 'http://127.0.0.1:8000/syncphealth'
    response_pg = requests.get(pg_url)
    data_pg = str(json.loads(response_pg.text))
    redis_url = 'http://127.0.0.1:8000/syncrhealth'
    response_redis = requests.get(redis_url)
    data_redis = str(json.loads(response_redis.text))
    final_data = data_pg + data_redis
    return {final_data}
##################################################################
# To complete Task5
@app.get("/postgresfetch")
def postgresFetchRecords():
    db = SessionLocal()
    try:
        sql = f"select * from {postgres_table} where phone=9000516507"
        df = pd.read_sql(sql, con=engine)
        json_data = json.dumps(json.loads(df.to_json(orient="records")))
        return {
            "Data": json_data
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        msg = str(e)
        return {
            "Postgres status": f"ERROR - {msg}"
        }
    finally:
        db.close()
##################################################################
# To complete Task9
@app.get("/mainappstatusdockercompose")
def get_other_server_status_docker():
    # Since port mapping is done, if we observe in docker compose file - will are tweaking the usual url
    url = 'http://businessmicroservice:8901/currentmainstatusdockercompose' # Using 8901 as that is where we are turning on our main app server when we use Dockerfile or docker-compose... Since it is inter-service communication inside container itself so our url is slightly difference - more details in readme
    response = requests.get(url)
    print(f"Status of main app server: {response.status_code}")
    data = json.loads(response.text)
    return data

##################################################################
# To complete Task10
@app.get("/bmserviceserverstatus")
def get_bmservice_server_status_docker():
    return {"businessMicroservice FastAPI app.py server status: Healthy"}

##################################################################
# To complete Task12 - Postgres part

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Note: Reason why done ~ https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
from models.postgresModels import UserModel # has SQLAlchemy ORM models
from schemas.postgresSchemas import UserBaseSchema, UserCreateSchema, UserUpdateSchema, UserSchema # has Pydantic models
from operations.crudOperationsPostgresdb import get_user, get_users, create_user, update_user, delete_user
from operations.crudOperationsRedisdb import get_user_redis, create_user_redis, update_user_redis, delete_user_redis, get_users_redis
from database.postgresDbConfig import DATABASE_URL, engine, SessionLocal, Base, postgres_table, get_db
from datetime import datetime

Base.metadata.create_all(bind=engine) # The models.Base.metadata.create_all(bind=engine) line is a convenient and powerful way to ensure your database schema is created and kept in sync with your SQLAlchemy models. It abstracts away the need to write raw SQL for table creation, making your code cleaner and more maintainable.

@app.post("/users/", response_model=UserSchema)
# FastAPI’s Response Models enable you to articulate the data structure that your API will provide in response to requests. When a client makes an HTTP request to the server, the server is required to send relevant data back to the client. The Response Models play a vital role in defining the details of this data model, ensuring consistency in API responses.
def create_user_postApi(user: UserCreateSchema, db: Session = Depends(get_db)):
    print('Postgres POST API call done')
    return create_user(db=db, user=user)

# Notice previous was POST API call with /users endpoint, now we have GET API call
@app.get("/users/", response_model=list[UserSchema])
def read_users_getApi(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    print('Postgres GET API call for all users done')
    return users

@app.get("/users/{user_id}", response_model=UserSchema)
def read_user_getApi(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print('Postgres GET API call for a user done')
    return db_user

@app.put("/users/{user_id}", response_model=UserSchema)
def update_user_putApi(user_id: int, user: UserUpdateSchema, db: Session = Depends(get_db)):
    db_user = update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print('Postgres PUT API call for a user done')
    return db_user

@app.delete("/users/{user_id}", response_model=UserSchema)
def delete_user_deleteApi(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print('Postgres DELETE API call for a user done')
    return db_user


####--------------------------------------------------------------####
# To complete Task12 (CONTINUED) - Redis part
# Similar to taking some reference from postgres part, rest is Redis specific function usecase

@app.post("/redisusers/", response_model=UserSchema)
def create_user_postApi_redis(user: UserCreateSchema):
    print('Redis POST API call done')
    return create_user_redis(user=user)

@app.get("/redisusers/", response_model=list[UserSchema])
def read_users_getApi(skip: int = 0, limit: int = 10):
    users = get_users_redis(skip=skip, limit=limit)
    print('Redis GET API call done')
    return users

@app.get("/redisusers/{user_id}", response_model=UserSchema)
def read_user_getApi_redis(user_id: int):
    db_user = get_user_redis(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print('Redis GET API call for a user done')
    return db_user

@app.put("/redisusers/{user_id}", response_model=UserSchema)
def update_user_putApi_redis(user_id: int, user: UserUpdateSchema):
    db_user = update_user_redis(user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print('Redis PUT API call for a user done')
    return db_user

@app.delete("/redisusers/{user_id}", response_model=UserSchema)
def delete_user_deleteApi_redis(user_id: int):
    db_user = delete_user_redis(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print('Redis DELETE API call for a user done')
    return db_user


##################################################################


##################################################################


##################################################################


##################################################################


##################################################################


##################################################################


##################################################################
















import json
from fastapi import FastAPI
import requests
import pandas as pd
from sqlalchemy import *
from database.postgresDbConfig import engine, SessionLocal, postgres_table
from database.redisDbConfig import rd
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



##################################################################


##################################################################


##################################################################


##################################################################


##################################################################


##################################################################


##################################################################


##################################################################


##################################################################


##################################################################
















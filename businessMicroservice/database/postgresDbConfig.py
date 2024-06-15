import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
import os
from os import environ as env

"""
Defining the postgres database configs. 
"""
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 7002
POSTGRES_USER = "postgresdluser"
POSTGRES_PASSWORD = "1234"
POSTGRES_DB = "fapidb"
# DATABASE_URL = os.getenv("POSTGRES_DB_URL", "None") # Way 1: second arg is the default value to return. POSTGRES_DB_URL is env variable defined in local environment in terminal, it has the same value as below. I have defined it using export POSTGRES_DB_URL="postgresql://postgresdluser:1234@localhost:7002/fapidb"; And later using os.getenv() code to extract value. Current way or below way works!.
# DATABASE_URL = env['ENV_DATABASE_URL'] # Way 2:  another way, we can define a .env variable in our project (which I have done for reference/learning, notice I have not added any space there...) and extract the variable from there as well
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}" # Way 3: Explicitly defining the db url. We are using port 7002 as we have defined when we spawned up the postgres container - remember readme doc step.
engine = _sql.create_engine(DATABASE_URL)
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = _declarative.declarative_base()
postgres_table = "tpsqltable" # this table is created in the db; when we logged in to the postgres container; we are defining it in the current config iself, to be able to use it globally

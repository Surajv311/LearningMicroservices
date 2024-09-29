import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
import os
from os import environ as env

"""
Defining the postgres database configs. 
"""

## For Task2
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
Base = _declarative.declarative_base() # database.Base is commonly associated with SQLAlchemy, which is a popular SQL toolkit and Object-Relational Mapping (ORM) library for Python. In SQLAlchemy, Base is usually defined using the declarative_base function. This function is used to create a base class for declarative class definitions. Declarative class definitions are a way to define database tables in Python by creating classes.
postgres_table = "tpsqltable" # this table is created in the db; when we logged in to the postgres container; we are defining it in the current config iself, to be able to use it globally

#################################################################################
## For Task7
## If we run dockerized version of this service in that case, I have defined an env variable in dockerfile APP_MODE_DOCKER, since its env, I will check in if below condition is true, in that case, postgres configs change so that our fastapi microservice is able to connect to other postgres microservice
## I have kept in mind similar env variable does not exist in my local macbook, else it will create confusion
## Also comments, defined in previous code, I am removing from below to keep things clean
if os.getenv("APP_MODE_DOCKER", "None") == 'docker_mode': # this condition means if we get value from APP_MODE_DOCKER we use it, else default value is None
    POSTGRES_HOST = "192.168.29.72"
    POSTGRES_PORT = 7002
    POSTGRES_USER = "postgresdluser"
    POSTGRES_PASSWORD = "1234"
    POSTGRES_DB = "fapidb"

# For Task8
if os.getenv("APP_MODE_DOCKER", "None") == 'docker_compose_mode': # we have defined this variable in the compose file
    POSTGRES_HOST = os.getenv('POSTGRES_HOST') # fetching variables using os.getenv() as we have defined them in compose file for fastapi env so the variables will exist in the container environment and can be picked up. If we log into our application container shell - we can do printenv and see all variables
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = _sql.create_engine(DATABASE_URL)
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = _declarative.declarative_base() # database.Base is commonly associated with SQLAlchemy, which is a popular SQL toolkit and Object-Relational Mapping (ORM) library for Python. In SQLAlchemy, Base is usually defined using the declarative_base function. This function is used to create a base class for declarative class definitions. Declarative class definitions are a way to define database tables in Python by creating classes.
postgres_table = "tpsqltable"

########################
# To complete Task12
# below function would ensure session continues until a function is exited - basically manages lifecycle of database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Other values like DATABASE_URL, engine, etc., will be picked up when I run the docker compose file as usual

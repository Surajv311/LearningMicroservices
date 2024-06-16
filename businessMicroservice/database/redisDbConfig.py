import redis
import os
from os import environ as env

"""
Defining the redis database configs. 
"""

## For Task2
REDIS_HOST = "localhost"
REDIS_PORT = 7001
REDIS_USER = None
REDIS_PASSWORD = None
REDIS_DB = None

# For Task7
## If we run dockerized version of this service in that case, I have defined an env variable in dockerfile APP_MODE_DOCKER, since its env, I will check in if below condition is true, in that case, redis configs change so that our fastapi microservice is able to connect to other redis microservice
if os.getenv("APP_MODE_DOCKER", "None") == 'docker_mode':
    REDIS_HOST = "192.168.29.72"
    REDIS_PORT = 7001
    REDIS_USER = None
    REDIS_PASSWORD = None
    REDIS_DB = None

if os.getenv("APP_MODE_DOCKER", "None") == 'docker_compose_mode': # we have defined this variable in the compose file
    REDIS_HOST = os.getenv('REDIS_HOST') # fetching variables using os.getenv() as we have defined them in compose file so the variables will exist in the container environment and can be picked up. If we log into our application container shell - we can do printenv and see all variables
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_USER = None
    REDIS_PASSWORD = None
    REDIS_DB = None

rd = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

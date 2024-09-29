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

# To complete Task12
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
# Similar to rd above; (check below comment for some info)
"""
decode_responses=True; This argument ensures that all responses from the Redis server are automatically decoded 
from bytes to strings. This is particularly useful because Redis, by default, stores and returns data as bytes, 
which can be cumbersome to handle in a Python application that predominantly uses strings.
Eg: 
redis_client.set('key', 'value')
value = redis_client.get('key') # Get the value (without decode_responses=True)
print(value)  # Output: b'value'
decoded_value = value.decode('utf-8') # Manually decode the value
print(decoded_value) # Output: 'value'

Else, use decode_responses=True argument. 

Note: We could also use something like this in our app.py file for businessMicroservice;
In FastAPI, the @app.on_event("startup") decorator is used to define functions that should run when the application starts up. These functions are typically used to perform initialization tasks, such as setting up database connections, loading configuration settings, or preparing any resources that the application needs to function.
@app.on_event("startup")
def startup_event():
    global redis_client
    ## redis_client = Redis(host='redislocalcontainer', port=6379, decode_responses=True)
    redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
"""

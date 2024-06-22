import sys
import os
from datetime import datetime
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.redisDbConfig import redis_client
## **Note below that we are importing the same schemas & models we used for validation in Postgres, here as well.**
from schemas.postgresSchemas import UserBaseSchema, UserCreateSchema, UserUpdateSchema, UserSchema # has Pydantic models
from models.postgresModels import UserModel

# To complete Task12
def create_user_redis(user: UserCreateSchema):
    redis_id = redis_client.incr("redis_id_value")  # Automatically increment redis_id. The redis.incr("redis_id") command in Redis is used to increment the value of the key "redis_id" by one and return the new value. You can use a different tag or key for your ID generation. Redis will not forget the value as long as the data is persisted correctly and the Redis server is not cleared or restarted without persistence enabled.
    user_data = user.dict() # converting the data we get into dict which aligns with UserCreateSchema
    user_data['id'] = redis_id # creating a key-value pair in the user_data dict having id key - unique id everytime data is added of a user and redis_id value
    user_data['created_at'] = datetime.utcnow().isoformat() # creating another key in our existing dict
    user_key_redis = f'user:{redis_id}' # since redis is nosql db, assigning a key specific for redis to identify
    redis_client.set(user_key_redis, json.dumps(user_data)) # json dumps: Converts a subset of Python objects into a json string. Not all objects are convertible and you may need to create a dictionary of data you wish to expose before serializing to JSON.
    return user_data

def get_users_redis(skip: int = 0, limit: int = 10):
    user_keys_redis = redis_client.keys("user:*") # If we recall in above code we are setting redis keys like: user_key_redis = f'user:{redis_id}' -> then doing redis_client.set()
    users = []
    for key in user_keys_redis[skip: skip + limit]:
        user_data = redis_client.get(key)
        if user_data:
            users.append(json.loads(user_data))
    return users

def get_user_redis(user_id: int):
    redis_key_format = f"user:{user_id}"
    user_data = redis_client.get(redis_key_format)
    if user_data is None:
        return None
    data = json.loads(user_data)
    return data

def update_user_redis(user_id: int, user: UserUpdateSchema):
    redis_key_format = f"user:{user_id}"
    user_data = redis_client.get(redis_key_format) ## using get() to check if key exists, later we set/update key if exists
    if not user_data:
        return None
    updated_data = user.dict()
    updated_data['id'] = user_id
    updated_data['created_at'] = json.loads(user_data)['created_at'] # extracting created_at from user_data which existed and adding it to updated_at data, which will later be serialized into a json string
    redis_client.set(redis_key_format, json.dumps(updated_data))
    return updated_data

def delete_user_redis(user_id: int):
    redis_key_format = f"user:{user_id}"
    user_data = redis_client.get(redis_key_format)
    if not user_data:
        return None
    redis_client.delete(redis_key_format)
    return json.loads(user_data)

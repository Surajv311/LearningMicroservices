import sys
import os
from datetime import datetime
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.redisDbConfig import redis_client
## **Note below that we are importing the same schemas we used for validation in Postgres, here as well.**
from schemas.postgresSchemas import UserBaseSchema, UserCreateSchema, UserUpdateSchema, UserSchema # has Pydantic models

# To complete Task12
def create_user_redis(user: UserCreateSchema):
    redis_id = redis_client.incr("redis_id_value")  # Automatically increment redis_id. The redis.incr("redis_id") command in Redis is used to increment the value of the key "redis_id" by one and return the new value. You can use a different tag or key for your ID generation. Redis will not forget the value as long as the data is persisted correctly and the Redis server is not cleared or restarted without persistence enabled.
    user_data = user.dict() # converting the data we get into dict which aligns with UserCreateSchema
    user_data['id'] = redis_id # creating a key-value pair in the user_data dict having id key - unique id everytime data is added of a user and redis_id value
    user_data['created_at'] = datetime.utcnow().isoformat() # creating another key in our existing dict
    user_key_redis = f'user:{redis_id}' # since redis is nosql db, assigning a key specific for redis to identify
    redis_client.set(user_key_redis, json.dumps(user_data)) # json dumps: Converts a subset of Python objects into a json string. Not all objects are convertible and you may need to create a dictionary of data you wish to expose before serializing to JSON.
    schema_validated_data = UserSchema(**user_data)
    """
    UserSchema(**user_data) will deserialize the JSON string into a dictionary, then unpack it into a UserSchema object. 
    We are doing this because later the FastAPI code validates the same in pydantic for the endpoint.
    Recall we have defined response_model=UserSchema, which means response should adhere to the UserSchema, same we are doing here as well
    It can be done in other way like: 
    deserialized_data = json.loads(user_data) ## loads() method can be used to parse a valid JSON string and convert it into a Python Dictionary.
    deserialized_obj = UserSchema(id=deserialized_data["id"], name=deserialized_data["name"], type=deserialized_data["type"], phone=deserialized_data["phone"], address=deserialized_data["address"], created_at=deserialized_data["created_at"])            
    Later, return deserialized_obj... 
    """
    return schema_validated_data

def get_users_redis(skip: int = 0, limit: int = 10):
    user_keys_redis = redis_client.keys("user:*") # If we recall in above code we are setting redis keys like: user_key_redis = f'user:{redis_id}' -> then doing redis_client.set()
    users = []
    for key in user_keys_redis[skip: skip + limit]:
        user_data = redis_client.get(key)
        if user_data:
            data = json.loads(user_data)
            schema_validated_data = UserSchema(**data)
            users.append(schema_validated_data) ## data validation being done for response_model
    return users

def get_user_redis(user_id: int):
    redis_key_format = f"user:{user_id}"
    user_data = redis_client.get(redis_key_format)
    if user_data is None:
        return None
    data = json.loads(user_data)
    schema_validated_data = UserSchema(**data)
    return schema_validated_data

def update_user_redis(user_id: int, user: UserUpdateSchema):
    redis_key_format = f"user:{user_id}"
    user_data = redis_client.get(redis_key_format) ## using get() to check if key exists, later we set/update key if exists
    if not user_data:
        return None
    updated_data = user.dict()
    updated_data['id'] = user_id
    updated_data['created_at'] = json.loads(user_data)['created_at'] # extracting created_at from user_data which existed and adding it to updated_at data, which will later be serialized into a json string
    redis_client.set(redis_key_format, json.dumps(updated_data))
    schema_validated_data = UserSchema(**updated_data)
    return schema_validated_data

def delete_user_redis(user_id: int):
    redis_key_format = f"user:{user_id}"
    user_data = redis_client.get(redis_key_format)
    if not user_data:
        return None
    redis_client.delete(redis_key_format)
    schema_validated_data = UserSchema(**json.loads(user_data))
    return schema_validated_data

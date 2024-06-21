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
def get_user_redis(user_id: int):
    user_data = redis_client.get(user_id) # Retrieve the JSON string from Redis
    if user_data:
        deserialized_obj = UserModel(**json.loads(user_data)) # Deserialize the JSON string into a dictionary, then unpack it into a User object
        """
        ## The other way is the standard way:
        deserialized_data = json.loads(user_data)
        deserialized_obj = UserModel(id=deserialized_data["id"], name=deserialized_data["name"], type=deserialized_data["type"], phone=deserialized_data["phone"], address=deserialized_data["address"], created_at=deserialized_data["created_at"])            
        ##  then we can return deserialized_obj
        """
        return deserialized_obj
    return None

def create_user_redis(user: UserCreateSchema):
    user_id = redis_client.incr("id")  # Automatically increment user ID
    created_at = datetime.utcnow()
    user_data = UserModel(id=user_id, created_at=created_at, **user.dict())
    redis_client.set(user_id, user_data.json())
    return user_data

def update_user_redis(user_id: int, user: UserUpdateSchema):
    existing_user = get_user_redis(user_id)
    if existing_user:
        updated_user = existing_user.copy(update=user.dict())
        redis_client.set(user_id, updated_user.json())
        return updated_user
    return None

def delete_user_redis(user_id: int):
    user = get_user_redis(user_id)
    if user:
        redis_client.delete(user_id)
        return user
    return None

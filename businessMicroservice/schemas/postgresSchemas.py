from pydantic import BaseModel
from datetime import datetime

#To complete Task12
class UserBaseSchema(BaseModel):
    # Pydantic models are simply classes which inherit from BaseModel and define fields as annotated attributes. A Pydantic BaseModel is a class that defines how your data looks like and the validation requirements it needs to pass in order to be valid.
    name: str
    type: str
    phone: int
    address: str
    # UserBase includes fields that are common to both creating and updating entities, excluding fields like id and created_at which are typically managed by the database.
class UserCreateSchema(UserBaseSchema):
    # UserCreate is used for input when creating a new entity. It inherits from UserBase and includes only the fields necessary for creating an entity (excluding id and created_at - as these attributes we will pass as a part of API call to create).
    pass

class UserUpdateSchema(UserBaseSchema):
    # UserUpdate is used for input when updating an existing entity. It also inherits from UserBase and excludes id and created_at - as these attributes we will pass as a part of API call to update.
    pass

class UserSchema(UserBaseSchema):
    # UserSchema is used for output when reading an entity from the database. It includes all the fields, including id and created_at.
    # Recall that we have similar User class defined in postgresModels.py file as well
    id: int
    created_at: datetime
    class Config:
        # The Config class with orm_mode = True in Pydantic schemas is added to enable compatibility with SQLAlchemy models. When working with SQLAlchemy ORM models, the data returned from the database queries are instances of SQLAlchemy models. By default, Pydantic expects plain dictionaries for its models. Setting orm_mode = True allows Pydantic models to be populated from ORM objects, enabling seamless data interchange between SQLAlchemy models and Pydantic schemas. It ensures that Pydantic can serialize SQLAlchemy models directly, which is particularly useful for API responses where SQLAlchemy objects need to be converted to JSON. This tells Pydantic to treat ORM models as dictionaries for serialization and deserialization. When a SQLAlchemy model instance is passed to a Pydantic schema, it knows how to extract the data.
        # Defining a Config class inside a Pydantic model class is valid and a common practice in Pydantic.
        # A class defined inside another class is known as an inner class in Python. If the inner class is instantiated, the object of the inner class can also be used by the parent class. The object of the inner class becomes one of the attributes of the outer class. The inner class automatically inherits the attributes of the outer class without formally establishing inheritance. The inner class has a local scope. It acts as one of the attributes of the outer class.
        # Interesting article: https://www.reddit.com/r/FastAPI/comments/lmywl6/orm_or_pydantic_model/
        # Recall we use Base ORM from sqlalchemy, to have better type validation we are using pydantic ORM here as well - with orm_mode True pydantic knows if any translation needs to be done for validation
        orm_mode = True

## NOTE: The above schemas are commonly used for both Postgres CRUD APIs and Redis CRUD APIs construction.

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Note: Reason why done ~ https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
from database.postgresDbConfig import Base # Base is ORM we use from sqlalchemy

#For Task12
class UserModel(Base):
    # We know Base is the ORM we are using
    """
    From Readme we know how our sql table looks like:
       Column   |            Type
    ------------+-----------------------------+
     id         | integer                     |
     name       | text                        |
     type       | text                        |
     phone      | integer                     |
     address    | character varying(300)      |
     created_at | timestamp without time zone |
    """
    __tablename__ = 'tpsqltable' # syntax when using Base class
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    type = Column(Text, index=True)
    phone = Column(Integer, index=True)
    address = Column(String(300), index=True)
    created_at = Column(TIMESTAMP, index=True)

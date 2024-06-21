from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Note: Reason why done ~ https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
from database.postgresDbConfig import Base # Base is ORM we use from sqlalchemy

#To complete Task12
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
    # Observe TIMESTAMP is capital: The rudimental types have “CamelCase” names such as String, Numeric, Integer, and DateTime. All of the immediate subclasses of TypeEngine are “CamelCase” types. The “CamelCase” types are to the greatest degree possible database agnostic, meaning they can all be used on any database backend where they will behave in such a way as appropriate to that backend in order to produce the desired behavior. In contrast to the “CamelCase” types are the “UPPERCASE” datatypes. These datatypes are always inherited from a particular “CamelCase” datatype, and always represent an exact datatype. When using an “UPPERCASE” datatype, the name of the type is always rendered exactly as given, without regard for whether or not the current backend supports it. Therefore the use of “UPPERCASE” types in a SQLAlchemy application indicates that specific datatypes are required, which then implies that the application would normally, without additional steps taken, be limited to those backends which use the type exactly as given. Examples of UPPERCASE types include VARCHAR, NUMERIC, INTEGER, and TIMESTAMP, which inherit directly from the previously mentioned “CamelCase” types String, Numeric, Integer, and DateTime, respectively. The “UPPERCASE” datatypes that are part of sqlalchemy.types are common SQL types that typically expect to be available on at least two backends if not more.
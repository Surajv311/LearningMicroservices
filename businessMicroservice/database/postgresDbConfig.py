import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

"""
Defining the postgres database configs. 
"""
DATABASE_URL = "postgresql://postgresdluser:1234@localhost:7002/fapidb" # explicitly using port 7002 as we have defined when we spawn up the container
engine = _sql.create_engine(DATABASE_URL)
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = _declarative.declarative_base()
postgres_table = "tpsqltable" # this table is created in the db; when we logged in to the postgres container; we are defining it in the current config iself, to be able to use it globally

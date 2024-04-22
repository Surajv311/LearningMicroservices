import datetime as _dt
import sqlalchemy as _sql

import database as _database


class PTempTable(_database.Base):
    __tablename__ = "tpsqltable"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, index=True)
    type = _sql.Column(_sql.String, index=True)
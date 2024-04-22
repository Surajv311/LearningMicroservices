import datetime as _dt
import pydantic as _pydantic


class _BaseData(_pydantic.BaseModel):
    name: str
    type: str

class _PData(_BaseData): # inheriting from basedata class
    id: int
    class Config:
        orm_mode = True

class _createData(_BaseData):
    pass
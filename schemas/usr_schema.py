import datetime as _dt
import pydantic as _pydantic

class _UserBase(_pydantic.BaseModel):
    email: str

class UserCreate(_UserBase):
    hashed_password: str
    model_config = _pydantic.ConfigDict(from_attributes=True)

class User(_UserBase):
    id: int
    model_config = _pydantic.ConfigDict(from_attributes=True)

class _LeadBase(_pydantic.BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str
    note: str

class LeadCreate(_LeadBase):
    pass

class Lead(_LeadBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_updated: _dt.datetime
    model_config = _pydantic.ConfigDict(from_attributes=True)
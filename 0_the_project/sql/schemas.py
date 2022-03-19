from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    address: str
    face_encoding: str
    created_at: datetime

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
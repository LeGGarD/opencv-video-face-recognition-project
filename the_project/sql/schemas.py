from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class FaceEncodingBase(BaseModel):
    face_encoding: str


class FaceEncodingCreate(FaceEncodingBase):
    pass


class FaceEncoding(FaceEncodingBase):
    id: int
    user_id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    address: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    face_encodings: List[FaceEncoding] = []
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

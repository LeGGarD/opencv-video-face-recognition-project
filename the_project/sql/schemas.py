from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


# class FaceEncodingBase(BaseModel):
#     face_encoding: str
#     created_at: datetime
#
#
# class FaceEncodingCreate(FaceEncodingBase):
#     pass
#
#
# class FaceEncoding(FaceEncodingBase):
#     id: int
#     user_id: int
#
#     class Config:
#         orm_mode = True


class UserBase(BaseModel):
    name: str
    address: str
    created_at: Optional[datetime] = datetime.now()


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    # face_encodings: List[FaceEncoding] = []

    class Config:
        orm_mode = True

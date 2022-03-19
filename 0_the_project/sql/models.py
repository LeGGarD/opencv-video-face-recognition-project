from datetime import datetime
from sqlalchemy import Integer, String, Column, DateTime

from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(70))
    address = Column(String(100))
    face_encoding = Column(String(150))
    created_at = Column(DateTime, default=datetime.utcnow())

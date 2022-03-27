from datetime import datetime
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(70))
    address = Column(String(100))
    face_encodings = relationship('FaceEncoding')
    created_at = Column(DateTime, default=datetime.utcnow())

class FaceEncoding(Base):
    __tablename__ = 'face_encodings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    face_encoding = Column(String(3072))
    created_at = Column(DateTime, default=datetime.utcnow())


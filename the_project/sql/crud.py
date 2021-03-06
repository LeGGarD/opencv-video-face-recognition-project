from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def get_user_by_address(db: Session, address: str):
    return db.query(models.User).filter(models.User.address == address).first()

def get_user_by_name_and_address(db: Session, name: str, address: str):
    return db.query(models.User).filter(models.User.address == address, models.User.name == name).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, address=user.address)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)
    db.commit()
    return True

def update_user_name(db: Session, user_id: int, name: str):
    user = get_user(db=db, user_id=user_id)
    user.name = name
    db.commit()
    return True

def update_user_address(db: Session, user_id: int, address: str):
    user = get_user(db=db, user_id=user_id)
    user.address = address
    db.commit()
    return True

def create_user_face_encoding(db: Session, face_encoding: schemas.FaceEncodingCreate, user_id: int):
    db_face_encoding = models.FaceEncoding(**face_encoding.dict(), user_id=user_id)
    db.add(db_face_encoding)
    db.commit()
    db.refresh(db_face_encoding)
    return db_face_encoding

def get_face_encodings_by_user_id(db: Session, user_id: int):
    face_encodings = db.query(models.FaceEncoding).filter(models.FaceEncoding.user_id == user_id).all()
    return face_encodings

def delete_face_encoding_by_user_id(db: Session, user_id: int):
    face_encodings = db.query(models.FaceEncoding).filter(models.FaceEncoding.user_id == user_id).all()
    print(f'sql.crud.delete_face_encoding_by_user_id(): Deleting {len(face_encodings)} encodings of User with id {user_id}')
    for face_encoding in face_encodings:
        db.delete(face_encoding)
        db.commit()
    return True

def get_face_encodings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FaceEncoding).offset(skip).limit(limit).all()

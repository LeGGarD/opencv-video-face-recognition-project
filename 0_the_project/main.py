from fastapi import FastAPI,  Depends, HTTPException
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from resources.resource_recognize_faces import router_main
from sql.database import Base, engine, SessionLocal
from sql import schemas, crud

from typing import List

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router_main)

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_address(db, address=user.address)
    if db_user:
        raise HTTPException(status_code=400, detail='Address is already registred')
    return crud.create_user(db=db, user=user)

@app.get('/users/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)

@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


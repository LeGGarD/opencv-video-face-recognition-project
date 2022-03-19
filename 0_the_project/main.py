from fastapi import FastAPI,  Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

from resources.resource_recognize_faces import router_main
from sql.database import Base, engine, SessionLocal
from sql import schemas, crud

from typing import List

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
app.include_router(router_main)

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/admin/', response_class=HTMLResponse)
def view_users_table(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return templates.TemplateResponse('admin.html', {'request': request, 'users': users})

@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_name = crud.get_user_by_name(db, name=user.name)
    db_user_address = crud.get_user_by_address(db, address=user.address)
    if db_user_address and db_user_name:
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


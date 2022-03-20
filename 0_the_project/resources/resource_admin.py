from fastapi import APIRouter, Depends, HTTPException
from typing import List

from starlette.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sql.database import Base, engine, SessionLocal
from sql import schemas, crud

router_admin = APIRouter()

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router_admin.get('/admin/', response_class=HTMLResponse)
def view_page(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return templates.TemplateResponse('admin.html', {'request': request, 'users': users})


@router_admin.get('/users/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)


@router_admin.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router_admin.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_name = crud.get_user_by_name(db, name=user.name)
    db_user_address = crud.get_user_by_address(db, address=user.address)
    if db_user_address and db_user_name:
        raise HTTPException(status_code=400, detail='Name and address is already registred')
    return crud.create_user(db=db, user=user)


@router_admin.get('/users/delete/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db=db, user_id=user_id)
    response = RedirectResponse(url='/admin/')
    return response

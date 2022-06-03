from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import json

from sqlalchemy.orm import Session
from sql import crud, schemas
from resources.resource_webcam_stream import update_face_rec_db

router_add_user = APIRouter()
templates = Jinja2Templates(directory="templates")


@router_add_user.get('/add_user/', response_class=HTMLResponse)
def get_add_user_page(request: Request):
    return templates.TemplateResponse('add_user.html', {'request': request})


@router_add_user.post('/add_user/')
def submit_form(name: str = Form(...), address: str = Form(...), encodings: str = Form(...),
                db: Session = Depends(crud.get_db)):
    # Adding new User
    user = schemas.UserCreate(name=name, address=address)
    db_user_name = crud.get_user_by_name(db=db, name=user.name)
    db_user_address = crud.get_user_by_address(db=db, address=user.address)
    if db_user_address and db_user_name:
        raise HTTPException(status_code=400, detail='Name and address is already registered')
    crud.create_user(db=db, user=user)

    # Adding Face Encodings
    user_id = crud.get_user_by_name_and_address(db=db, name=name, address=address)
    user_encodings = []
    for encoding in encodings.split('],['):
        if encoding[0] != '[':
            encoding = '[' + encoding
        if encoding[-1] != ']':
            encoding = encoding + ']'
        face_encoding = schemas.FaceEncodingCreate(face_encoding=encoding)
        crud.create_user_face_encoding(db=db, face_encoding=face_encoding, user_id=user_id.id)
        user_encodings.append(json.loads(encoding))

    # Updating Face Rec Algorithm's Data Base
    update_face_rec_db(user_encodings, name, address)

    return PlainTextResponse('User and encodings were succesfully added!')

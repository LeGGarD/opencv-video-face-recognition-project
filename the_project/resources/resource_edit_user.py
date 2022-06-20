from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import json

from sqlalchemy.orm import Session
from sql import crud, schemas
from resources.resource_webcam_stream import reload_face_rec_db

router_edit_user = APIRouter()
templates = Jinja2Templates(directory="templates")


@router_edit_user.get('/edit_user/{user_id}')
def edit_user_page(request: Request, user_id: int, db: Session = Depends(crud.get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        return RedirectResponse(url='/admin/')
    return templates.TemplateResponse('edit_user.html', {'request': request, 'user': user})


@router_edit_user.post('/edit_user/{user_id}')
def proceed_esit_user_form(user_id: int, name: str = Form(...), address: str = Form(...), encodings: str = Form(...),
                           db: Session = Depends(crud.get_db)):
    # Update User info
    crud.update_user_name(db=db, user_id=user_id, name=name)
    crud.update_user_address(db=db, user_id=user_id, address=address)

    # Update encodings if they were changed
    if encodings != 'q':
        crud.delete_face_encoding_by_user_id(db=db, user_id=user_id)
        for encoding in encodings.split('],['):
            if encoding[0] != '[':
                encoding = '[' + encoding
            if encoding[-1] != ']':
                encoding = encoding + ']'
            face_encoding = schemas.FaceEncodingCreate(face_encoding=encoding)
            crud.create_user_face_encoding(db=db, face_encoding=face_encoding, user_id=user_id)

    # Updating Face Rec Algorithm's Data Base
    reload_face_rec_db()

    return RedirectResponse(url=f'/edit_user/{user_id}', status_code=200)

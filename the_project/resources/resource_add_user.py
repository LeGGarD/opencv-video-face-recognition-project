import time
from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette import status

from services.service_recognize_faces import RecognizeFaces
from services.service_get_webcam_stream import WebcamStream
from sql import crud, schemas

router_add_user = APIRouter()
templates = Jinja2Templates(directory="templates")

# recognize_faces = RecognizeFaces()
# webcam_stream = WebcamStream()


@router_add_user.get('/add_user_step_1/', response_class=HTMLResponse)
def get_add_user_page(request: Request):
    return templates.TemplateResponse('add_user_step_1.html', {'request': request})


@router_add_user.get('/add_user_step_2/{user_id}', response_class=HTMLResponse)
def get_add_user_page(request: Request, user_id: int):
    return templates.TemplateResponse('add_user_step_2.html', {'request': request, 'user_id': user_id})


# @router_add_user.post('/add_user_step_1/')
# def submit_form(name: str = Form(...), address: str = Form(...), db: Session = Depends(crud.get_db)):
#     user = schemas.UserCreate(name=name, address=address)
#     db_user_name = crud.get_user_by_name(db, name=user.name)
#     db_user_address = crud.get_user_by_address(db, address=user.address)
#     if db_user_address and db_user_name:
#         raise HTTPException(status_code=400, detail='Name and address is already registered')
#     crud.create_user(db=db, user=user)
#     user = crud.get_user_by_name_and_address(db=db, name=name, address=address)
#     user_id = user.id
#     return RedirectResponse(f'/add_user_step_2/{user_id}', status_code=status.HTTP_302_FOUND)


# @router_add_user.get('/add_user_step_2/recognize_face/{user_id}')
# def recognize_face(user_id: int, db: Session = Depends(crud.get_db)):
#     frame = webcam_stream.generated_frame()
#     encodings = recognize_faces.recognize_faces(frame)
#
#     if len(encodings) != 1:
#         print('resource_webcam_stream.recognize_face(): Face not found or found more than 1 face!')
#         return False
#     else:
#         face_encoding = schemas.FaceEncodingCreate()
#         face_encoding.face_encoding = str(list(encodings[0]))
#         crud.create_face_encoding(db=db, face_encoding=face_encoding, user_id=user_id)
#         return True


##################################################################################
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
    user_id = crud.get_user_by_name_and_address(db=db, name=db_user_name, address=db_user_address)
    for encoding in encodings.split('],['):
        if encoding[0] != '[':
            encoding = '[' + encoding
        elif encoding[-1] != ']':
            encoding = encoding + ']'
        # encoding.replace('[', '')
        # encoding.replace(']', '')
        face_encoding = schemas.FaceEncodingCreate(face_encoding=encoding)
        crud.create_user_face_encoding(db=db, face_encoding=face_encoding, user_id=user_id)
    print(crud.get_face_encodings_by_user_id(db=db, user_id=user_id))
    return PlainTextResponse('User and encodings were succesfully added!')



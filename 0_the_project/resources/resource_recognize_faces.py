from fastapi import APIRouter

from starlette.requests import Request
from starlette.responses import HTMLResponse, StreamingResponse
from starlette.templating import Jinja2Templates

import cv2

from services.service_recognize_faces import RecognizeFaces

router_main = APIRouter()
templates = Jinja2Templates(directory="templates")

face_rec = RecognizeFaces()

camera = cv2.VideoCapture(0)


def generate_frames():
    while True:

        ## read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.resize(frame, (960, 540), interpolation=cv2.INTER_CUBIC)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'
               + frame +
               b'\r\n')


@router_main.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router_main.get('/video')
def video():
    return StreamingResponse(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

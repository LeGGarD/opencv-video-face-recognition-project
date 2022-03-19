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


# ============================= A bit of kostyl =============================
def smart_resize(camera: cv2.VideoCapture, needed_height: int = 540):
    success, frame = camera.read()
    resolution = frame.shape
    coef = needed_height / resolution[0]
    return int(resolution[1] * coef), int(resolution[0] * coef)

frame_resolution = smart_resize(camera)
print(frame_resolution)
# ============================= A bit of kostyl =============================

def generate_frames():
    while True:

        ## read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.resize(frame, frame_resolution, interpolation=cv2.INTER_CUBIC)
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

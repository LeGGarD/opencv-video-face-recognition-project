from fastapi import APIRouter

from starlette.requests import Request
from starlette.responses import HTMLResponse, StreamingResponse, PlainTextResponse
from starlette.templating import Jinja2Templates

from services.service_get_webcam_stream import WebcamStream

router_main = APIRouter()
templates = Jinja2Templates(directory="templates")

webcam_stream = WebcamStream()


@router_main.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router_main.get('/video_start')
def video_start():
    try:
        webcam_stream.start_generating_frames()
    except:
        print('You tried to turn on the webcam and sucked')
    return PlainTextResponse('You just turned on the camera')


@router_main.get('/video')
def video():
    while True:
        if not webcam_stream.webcam:
            pass
        else:
            return StreamingResponse(webcam_stream.generated_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


@router_main.get('/video_stop')
def video_stop():
    try:
        webcam_stream.stop_generating_frames()
    except:
        print('You tried to turn off the webcam and sucked')
    return PlainTextResponse('You just turned off the camera')

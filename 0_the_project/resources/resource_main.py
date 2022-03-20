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
    return StreamingResponse(webcam_stream.generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


@router_main.get('/video_stop')
def video_stop():
    try:
        webcam_stream.stop_generating_frames()
    except:
        print('You tried to turn off the webcam and sucked')
    return PlainTextResponse('You just turned off the camera')

from fastapi import APIRouter

from starlette.requests import Request
from starlette.responses import HTMLResponse, StreamingResponse
from starlette.templating import Jinja2Templates

from services.service_get_webcam_stream import WebcamStream

router_main = APIRouter()
templates = Jinja2Templates(directory="templates")

webcam_stream = WebcamStream()


@router_main.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router_main.get('/video')
def video():
    return StreamingResponse(webcam_stream.generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

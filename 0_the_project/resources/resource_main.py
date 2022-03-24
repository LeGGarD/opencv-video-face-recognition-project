from fastapi import APIRouter, WebSocket
import asyncio

from starlette.requests import Request
from starlette.responses import HTMLResponse, PlainTextResponse
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
    webcam_stream.start_stream()
    return PlainTextResponse('You just turned on the camera')

@router_main.websocket("/ws_video")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            await asyncio.sleep(0.04)
            await websocket.send_bytes(webcam_stream.generated_frame())
        except:
            await asyncio.sleep(0.1)

@router_main.get('/video_stop')
def video_stop():
    webcam_stream.stop_stream()
    return PlainTextResponse('You just turned off the camera')

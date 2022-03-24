from fastapi import APIRouter, WebSocket
import asyncio
import cv2

from starlette.requests import Request
from starlette.responses import HTMLResponse, StreamingResponse, PlainTextResponse
from starlette.templating import Jinja2Templates

# from services.service_get_webcam_stream import WebcamStream

router_main = APIRouter()
templates = Jinja2Templates(directory="templates")

# webcam_stream = WebcamStream()


class WebcamStream():

    def __init__(self):
        self.webcam = None
        self.webcam_resolution = None

    def resize_webcam_resolution(self, frame, needed_height: int = 540):
        resolution = frame.shape
        coef = needed_height / resolution[0]
        return int(resolution[1] * coef), int(resolution[0] * coef)

    def start_stream(self):
        self.webcam = cv2.VideoCapture(0)
        _, frame = self.webcam.read()
        self.webcam_resolution = self.resize_webcam_resolution(frame)
        print(f'Webcam has turned on! With {self.webcam_resolution} resolution')

    def generated_frame(self):
        success, frame = self.webcam.read()
        frame = cv2.resize(frame, self.webcam_resolution, interpolation=cv2.INTER_CUBIC)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        return frame

    def stop_stream(self):
        self.webcam.release()
        print('Webcam has turned off!')

webcam_stream = WebcamStream()

@router_main.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router_main.get('/video_start')
def video_start():
    try:
        webcam_stream.start_stream()
    except:
        print('You tried to turn on the webcam and sucked')
    return PlainTextResponse('You just turned on the camera')


# @router_main.get('/video')
# def video():
#     while True:
#         if not webcam_stream.webcam:
#             pass
#         else:
#             return StreamingResponse(webcam_stream.generated_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


@router_main.websocket("/ws_video")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            await asyncio.sleep(0.04)
            await websocket.send_bytes(webcam_stream.generated_frame())
        except:
            await asyncio.sleep(2)
            print('Webcam is turned off')

@router_main.get('/video_stop')
def video_stop():
    try:
        webcam_stream.stop_stream()
    except:
        print('You tried to turn off the webcam and sucked')
    return PlainTextResponse('You just turned off the camera')

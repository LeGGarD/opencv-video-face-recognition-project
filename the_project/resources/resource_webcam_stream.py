from fastapi import APIRouter, WebSocket, Depends
from fastapi.responses import PlainTextResponse
import asyncio

from sqlalchemy.orm import Session

from services.service_get_webcam_stream import WebcamStream
from services.service_recognize_faces import RecognizeFaces
from sql import crud, schemas

router_webcam_stream = APIRouter()

webcam_stream = WebcamStream()
recognize_faces = RecognizeFaces()

@router_webcam_stream.websocket("/ws_video")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            await asyncio.sleep(0.04)
            await websocket.send_bytes(webcam_stream.generated_frame_bytes())
        except:
            await asyncio.sleep(0.1)

@router_webcam_stream.get('/video_start')
def video_start():
    webcam_stream.start_stream()
    return PlainTextResponse('You just turned on the camera')


@router_webcam_stream.get('/video_stop')
def video_stop():
    webcam_stream.stop_stream()
    return PlainTextResponse('You just turned off the camera')




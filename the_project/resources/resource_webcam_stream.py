import asyncio
from typing import List
from fastapi import APIRouter, WebSocket
from fastapi.responses import PlainTextResponse, HTMLResponse
from starlette.websockets import WebSocketDisconnect

from services.service_get_webcam_stream import WebcamStream
from services.service_recognize_faces import RecognizeFaces

router_webcam_stream = APIRouter()

webcam_stream = WebcamStream()
recognize_faces = RecognizeFaces()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, frame: bytes):
        for connection in self.active_connections:
            await connection.send_bytes(frame)


manager = ConnectionManager()


# WebSocket
@router_webcam_stream.websocket("/ws_video/{stream_type}")
async def websocket_endpoint(websocket: WebSocket, stream_type: int):
    await manager.connect(websocket)
    try:
        while True:
            # Set displaying FPS here as: 1 / FPS
            await asyncio.sleep(0.06)

            if stream_type == 1:
                frame = await webcam_stream.generate_frame_bytes()
            elif stream_type == 2:
                frame = await webcam_stream.generate_frame_face_rec()
            else:
                frame = None

            if frame is None:
                raise WebSocketDisconnect
            else:
                await manager.broadcast(frame)
    except WebSocketDisconnect:
        print('resource_webcam_stream.websocket_endpoint(): Raised WebSocketDisconnect')
        manager.disconnect(websocket)
        webcam_stream.stop_stream()


@router_webcam_stream.get('/video_start')
def video_start():
    webcam_stream.start_stream()
    return PlainTextResponse('You just turned on the camera')


@router_webcam_stream.get('/video_stop')
def video_stop():
    webcam_stream.stop_stream()
    return PlainTextResponse('You just turned off the camera')


@router_webcam_stream.get('/take_photo', response_class=HTMLResponse)
def take_photo() -> str or bool:
    photo = webcam_stream.generated_frame()
    if photo is None:
        print('resource_webcam_stream.recognize_face(): Couldn\'t take a photo, maybe webcam is turned off')
        return PlainTextResponse('')

    encodings = recognize_faces.recognize_faces(photo)

    if len(encodings) != 1:
        print('resource_webcam_stream.recognize_face(): Face not found or found more than 1 face!')
        return PlainTextResponse('')
    else:
        return str(list(encodings[0]))

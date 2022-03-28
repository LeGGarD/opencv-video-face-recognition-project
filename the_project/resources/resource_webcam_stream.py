import asyncio
from typing import List
from fastapi import APIRouter, WebSocket
from fastapi.responses import PlainTextResponse
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


@router_webcam_stream.websocket("/ws_video")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(0.04)
            frame = await webcam_stream.generated_frame_bytes()
            if frame is None:
                raise WebSocketDisconnect
            else:
                await manager.broadcast(frame)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router_webcam_stream.get('/video_start')
def video_start():
    webcam_stream.start_stream()
    return PlainTextResponse('You just turned on the camera')


@router_webcam_stream.get('/video_stop')
def video_stop():
    webcam_stream.stop_stream()
    return PlainTextResponse('You just turned off the camera')

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
import cv2
import face_recognition

from resources.resource_main import router_main
from resources.resource_admin import router_admin
from resources.resource_add_user import router_add_user

from services.service_get_webcam_stream import WebcamStream

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
app.include_router(router_main)
app.include_router(router_admin)
app.include_router(router_add_user)

templates = Jinja2Templates(directory="templates")
# webcam_stream = WebcamStream()
# webcam_stream.start_generating_frames()


# ==================================== WebSocket Video Streaming '/test' ====================================
html = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Python_Websocket_Live_Streaming</title>
    </head>
    <body onload="openSocket()">
        <div id="status">
            Connection failed. Somebody may be using the socket.
        </div>
        <div style="text-align: center">
            <canvas id="msg" width="720" height="540" style="display:inline-block" style="margin-left: auto; margin-right: auto;"/>
        </div>
            
        <script>
        function openSocket() {
            socket = new WebSocket("ws://127.0.0.1:8000/ws_video");
            let msg = document.getElementById("msg");
            socket.addEventListener('open', function (event) {
                document.getElementById("status").innerHTML = "Opened";
            });
            socket.addEventListener('message', function (event) {
                let context = msg.getContext("2d");
                let image = new Image();
                image.src = URL.createObjectURL(event.data);
                image.addEventListener("load", function (event) {
                    context.drawImage(image, 0, 0, msg.width, msg.height);
                });
            });
        }
        </script>
    </body>
</html>
'''

vid = cv2.VideoCapture(0)


def resize_webcam_resolution(frame, needed_height: int = 540):
    resolution = frame.shape
    coef = needed_height / resolution[0]
    return int(resolution[1] * coef), int(resolution[0] * coef)


success, frame = vid.read()
webcam_resolution = resize_webcam_resolution(frame)
print(webcam_resolution)


def generated_frame():
    success, frame = vid.read()

    # locations = face_recognition.face_locations(frame, model='small')
    #
    # for face_location in locations:
    #     top_left = (face_location[3], face_location[0])
    #     bottom_right = (face_location[1], face_location[2])
    #     color = [0, 255, 0]
    #     cv2.rectangle(frame, top_left, bottom_right, color, 3)

    frame = cv2.resize(frame, webcam_resolution, interpolation=cv2.INTER_CUBIC)
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()

    return frame


@app.get("/test")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws_video")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(0.04)
        await websocket.send_bytes(generated_frame())
# ==================================== WebSocket Video Streaming '/test' ====================================

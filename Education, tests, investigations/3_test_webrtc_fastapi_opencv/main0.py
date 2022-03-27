import asyncio
import os
import platform
import json

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay, MediaBlackhole

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.schemas import Offer

ROOT = os.path.dirname(__file__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

relay = None
webcam = None


def create_local_tracks(play_from=None):
    global relay, webcam

    if play_from:
        player = MediaPlayer(play_from)
        return player.audio, player.video
    # else:
    #     options = {"framerate": "30", "video_size": "1280x720"}
    #     if relay is None:
    #         if platform.system() == "Darwin":
    #             webcam = MediaPlayer(
    #                 "default:none", format="avfoundation", options=options
    #             )
    #         elif platform.system() == "Windows":
    #             webcam = MediaPlayer(
    #                 "video=Integrated Camera", format="dshow", options=options
    #             )
    #         else:
    #             webcam = MediaPlayer("/dev/video0", format="v4l2", options=options)
    #         relay = MediaRelay()
    #     return None, relay.subscribe(webcam.video)
    else:
        options = {"framerate": "30", "video_size": "1280x720"}
        if relay is None:
            webcam = MediaPlayer("/dev/video0", format="v4l2", options=options)
            relay = MediaRelay()
        return None, relay.subscribe(webcam.video)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/offer")
async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    # open media source
    audio, video = create_local_tracks()

    # handle offer
    await pc.setRemoteDescription(offer)

    # send answer
    answer = await pc.createAnswer()

    await pc.setRemoteDescription(offer)
    for t in pc.getTransceivers():
        if t.kind == "audio" and audio:
            pc.addTrack(audio)
        elif t.kind == "video" and video:
            pc.addTrack(video)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return json.dumps({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})


pcs = set()


@app.on_event("shutdown")
async def on_shutdown():
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

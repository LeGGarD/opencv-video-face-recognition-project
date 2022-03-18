from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from resources.resource_recognize_faces import router_main

app = FastAPI()

app.include_router(router_main)
app.mount("/static", StaticFiles(directory="static"), name="static")
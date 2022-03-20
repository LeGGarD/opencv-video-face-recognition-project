from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from resources.resource_recognize_faces import router_recognize_faces
from resources.resource_database import router_database

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
app.include_router(router_recognize_faces)
app.include_router(router_database)

from fastapi import FastAPI

from resources.resource_recognize_faces import router_main

app = FastAPI()

app.include_router(router_main)

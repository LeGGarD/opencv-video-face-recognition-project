from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from resources.resource_main import router_main
from resources.resource_admin import router_admin
from resources.resource_add_user import router_add_user

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
app.include_router(router_main)
app.include_router(router_admin)
app.include_router(router_add_user)

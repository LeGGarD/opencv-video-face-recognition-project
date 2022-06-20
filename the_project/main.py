from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from resources.resource_main import router_main
from resources.resource_admin import router_admin
from resources.resource_add_user import router_add_user
from resources.resource_webcam_stream import router_webcam_stream
from resources.resource_edit_user import router_edit_user

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
app.include_router(router_main)
app.include_router(router_admin)
app.include_router(router_add_user)
app.include_router(router_webcam_stream)
app.include_router(router_edit_user)

templates = Jinja2Templates(directory="templates")



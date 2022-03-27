from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router_add_user = APIRouter()
templates = Jinja2Templates(directory="templates")


@router_add_user.get('/add_user_step_1/', response_class=HTMLResponse)
def get_add_user_page(request: Request):
    return templates.TemplateResponse('add_user_step_1.html', {'request': request})

@router_add_user.post('/add_user_step_1/')
def recognize_face():
    pass

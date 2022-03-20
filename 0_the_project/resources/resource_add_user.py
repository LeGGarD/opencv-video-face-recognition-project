from fastapi import APIRouter

from starlette.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router_add_user = APIRouter()


@router_add_user.get('/add_user/', response_class=HTMLResponse)
def get_add_user_page(request: Request):
    return templates.TemplateResponse('add_user.html', {'request': request})

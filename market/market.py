from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from starlette import status

from auth.auth_functions import get_current_user
from database.redis_main import RedisTools


router = APIRouter(
    prefix='/market'
)


templates = Jinja2Templates(directory='templates')


@router.post('/choose_market')
async def parsers_menu(request: Request):
    user = await get_current_user(RedisTools.get_data('Authorization'))
    if user:
        return templates.TemplateResponse('parsers_menu.html', {'request': request})
    else:
        return {'detail': 'Not login'}


@router.get('/choose_market/{market}')
async def test(request: Request, market: str):
    return templates.TemplateResponse('category.html', {'request': request, 'error': None})

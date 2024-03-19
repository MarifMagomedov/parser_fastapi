import pickle
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.staticfiles import StaticFiles

from auth.auth_functions import get_current_user
from database.redis_main import RedisTools
from parsers.parser import MegaMarketParser


router = APIRouter(
    prefix='/market',
    tags=['/market']
)


templates = Jinja2Templates(directory='templates')
router.mount("/static/styles.css", StaticFiles(directory="static"), name="static")


@router.post('/choose_market')
async def parsers_menu(request: Request):
    user = await get_current_user(RedisTools.get_data('Authorization'))
    if user:
        return templates.TemplateResponse('parsers_menu.html', {'request': request})
    else:
        return {'detail': 'Not login'}


@router.get('/choose_market')
async def parsers_menu(request: Request):
    user = await get_current_user(RedisTools.get_data('Authorization'))
    if user:
        return templates.TemplateResponse('parsers_menu.html', {'request': request})
    else:
        return {'detail': 'Not login'}


@router.get('/choose_market/{market}')
async def search_category(request: Request, market: str, category: str = Form(None), send_message: str = Form(None)):
    RedisTools.set_data('market', market)
    return templates.TemplateResponse('category.html', {'request': request})


@router.post('/choose_market/{market}')
async def search_category(request: Request, market: str, category: str = Form(None), send_message: str = Form(None)):
    RedisTools.clear()
    if RedisTools.get_data(market):
        parse_items = pickle.loads(RedisTools.get_data(market))
    else:
        parse_items = MegaMarketParser.get_items(category)
        RedisTools.set_data(market, pickle.dumps(parse_items))
    return templates.TemplateResponse('category.html', {'request': request, 'items': parse_items})

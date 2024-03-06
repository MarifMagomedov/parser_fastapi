from typing import Annotated
import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.openapi.models import Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse

from auth.auth import router as auth_router
from auth.auth_functions import get_current_user
from database.database_main import database as db

app = FastAPI()


templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    db.create_tables()


@app.get('/')
async def parsers_menu(request: Request):
    print(request.cookies)
    user_token_active = await get_current_user(request.cookies.get('Authorization'))
    if user_token_active:
        return templates.TemplateResponse('parsers_menu.html', {'request': request})
    else:
        return {'detail': 'Not login'}


@app.get('/login')
async def login_page(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})


@app.get('/register')
async def register_page(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def not_auth_user(request, exc):
    return RedirectResponse('/login')


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

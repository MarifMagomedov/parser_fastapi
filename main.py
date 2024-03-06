import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse

from auth.auth import router as auth_router
from auth.auth_functions import get_current_user
from database.database_main import database as db
from market.market import router as market_router


app = FastAPI()


templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth_router)
app.include_router(market_router)


@app.on_event("startup")
async def startup():
    db.create_tables()


@app.get('/login')
async def login_page(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})


@app.get('/register')
async def register_page(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def not_auth_user(request, exc):
    return RedirectResponse('/login', status_code=status.HTTP_302_FOUND)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
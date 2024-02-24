from typing import Annotated

import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from auth.auth import router as auth_router
from auth.auth_functions import get_current_user
from database.database_main import Database

app = FastAPI()
db = Database()

templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")
user_dependency = Annotated[dict, Depends(get_current_user)]

app.include_router(auth_router)


@app.get('/')
async def auth_successful(user: user_dependency):
    if user is None:
        raise HTTPException(
            status_code=401,
            detail='Auth failed'
        )
    return {'User': user}


@app.get('/login')
async def login_page(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})


@app.get('/register')
async def register_page(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

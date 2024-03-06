from datetime import timedelta
from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import RedirectResponse
from typing import Annotated
from starlette import status
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates

from auth.auth_functions import authenticate_user, create_access_token
from database.database_main import database as db


router = APIRouter()


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
templates = Jinja2Templates(directory='templates')


@router.post('/register/successful', status_code=status.HTTP_201_CREATED)
async def create_user(request: Request, email: str = Form(), password: str = Form(), telegram: str = Form()):
    user = db.get_user_data(email)
    if not user:
        db.create_user(
            email=email,
            password=bcrypt_context.hash(password),
            telegram=telegram,
        )
        return templates.TemplateResponse('auth.html', {'request': request,
                                                        'accept_user_register_text': 'Вы успешно зарегистрировались! '
                                                                                     'Войдите в аккаунт'})
    return templates.TemplateResponse(
        'registration.html', {'request': request,
                              'error': 'Пользователь с таким адресом почты уже существует!'}
    )


@router.post('/login/token')
async def login_for_access_token(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    request: Request,
    response: Response
):
    user, error = (await authenticate_user(bcrypt_context, email, password)).values()
    if not user:
        return templates.TemplateResponse(
            'auth.html', {'request': request,
                          'error': error}
        )
    token = await create_access_token(user.email, user.id, timedelta(minutes=1))
    response.set_cookie(key='Authorization', value=token)
    return True

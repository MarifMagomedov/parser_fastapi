from datetime import timedelta
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from typing import Annotated
from starlette import status
from passlib.context import CryptContext

from auth.auth_functions import authenticate_user, create_access_token
from database.database_main import Database
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

router = APIRouter()

db = Database()
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
            user_agent=request.headers['User-Agent']
        )
        return templates.TemplateResponse('auth.html', {'request': request,
                                                        'accept_user_register_text': 'Вы успешно зарегистрировались! '
                                                                                     'Войдите в аккаунт'})
    return templates.TemplateResponse(
        'registration.html', {'request': request,
                              'error': 'Пользователь с таким адресом почты уже существует!'}
    )


@router.post('/login/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request):
    user, error = (await authenticate_user(bcrypt_context, form_data.username, form_data.password)).values()
    if not user:
        return templates.TemplateResponse(
            'auth.html', {'request': request,
                          'error': error}
        )
    token = await create_access_token(user.email, user.id, timedelta(days=1))
    db.update_user_token(token, user.email)
    return RedirectResponse()

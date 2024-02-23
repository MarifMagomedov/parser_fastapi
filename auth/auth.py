from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from typing import Annotated
from starlette import status
from passlib.context import CryptContext
from database.database_main import Database
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from auth.schemas import Token
from auth.auth_functions import authenticate_user, create_access_token

router = APIRouter()

db = Database()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
templates = Jinja2Templates(directory='templates')


@router.post('/register/user/', status_code=status.HTTP_201_CREATED)
async def create_user(request: Request, email: str = Form(), password: str = Form(), telegram: str = Form()):
    user = db.check_user_in_base(email)
    if not user:
        db.create_user(
            email=email,
            password=bcrypt_context.hash(password),
            telegram=telegram
        )
        return templates.TemplateResponse('auth.html', {'request': request,
                                                        'accept_user_register_text': 'Вы успешно зарегистрировались! '
                                                                                     'Войдите в аккаунт'})
    return templates.TemplateResponse(
        'registration.html', {'request': request,
                              'error': 'Пользователь с таким адресом почты уже существует!'}
    )


@router.post('/login/user/', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request):
    user, error = authenticate_user(bcrypt_context, form_data.username, form_data.password).values()
    if not user:
        return templates.TemplateResponse(
            'auth.html', {'request': request,
                          'error': error}
        )
    token = create_access_token(user.email, user.id, timedelta(minutes=1))
    return Token(token_type='bearer', access_token=token)

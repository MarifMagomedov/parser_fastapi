from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from config import load_auth_config
from database.models import User
from passlib.context import CryptContext
from database.database_main import Database
from datetime import timedelta, datetime


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')
config = load_auth_config()
db = Database()


def authenticate_user(bcrypt_context: CryptContext, email: str, password: str):
    user = db.check_user_in_base(email, get_user=True)
    request = {'user': '', 'error': ''}
    if not user:
        request.update({'error': 'Пользователя с такой почтой не существует!'})
    elif not bcrypt_context.verify(password, user.hashed_password):
        request.update({'error': 'Вы ввели неправильный пароль!'})
    else:
        request.update({'user': user})
    return request


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, config.secret_key, algorithm=config.algorithm)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.check_user_in_base(email)
    if not user:
        raise credentials_exception
    return user

from fastapi import HTTPException
from jose import jwt, JWTError
from starlette import status

from config import load_auth_config
from database.models import User
from passlib.context import CryptContext
from database.database_main import database as db
from datetime import timedelta, datetime


config = load_auth_config()


async def authenticate_user(bcrypt_context: CryptContext, email: str, password: str) -> dict:
    user = db.get_user_data(email)
    user_data = {'user': '', 'error': ''}
    if not user:
        user_data.update({'error': 'Пользователя с такой почтой не существует!'})
    elif not bcrypt_context.verify(password, user.hashed_password):
        user_data.update({'error': 'Вы ввели неправильный пароль!'})
    else:
        user_data.update({'user': user})
    return user_data


async def create_access_token(username: str, user_id: int, expires_delta: timedelta) -> jwt:
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, config.secret_key, algorithm=config.algorithm)


async def get_current_user(token: str) -> User:
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
    user = db.get_user_data(email)
    if not user:
        raise credentials_exception
    return user

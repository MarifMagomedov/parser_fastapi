from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    email: str
    password: str
    telegram: str


class Token(BaseModel):
    access_token: str
    token_type: str

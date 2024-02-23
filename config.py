from environs import Env
from dataclasses import dataclass


@dataclass
class Database:
    host: str
    port: str
    name: str
    user: str
    password: str


@dataclass
class AuthConfig:
    secret_key: str
    algorithm: str


def load_database_config() -> Database:
    env = Env()
    env.read_env()
    return Database(
        host=env('DB_HOST'),
        port=env('DB_PORT'),
        name=env('DB_NAME'),
        user=env('DB_USER'),
        password=env('DB_PASSWORD')
    )


def load_auth_config() -> AuthConfig:
    env = Env()
    env.read_env()
    return AuthConfig(
        secret_key=env('SECRET_KEY'),
        algorithm=env('ALGORITHM')
    )
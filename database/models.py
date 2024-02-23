from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from config import load_database_config
from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(primary_key=True)
    hashed_password: Mapped[str]
    telegram: Mapped[str]


class DatabaseConnect:
    def __init__(self):
        self.config = load_database_config()
        self.engine = create_engine(
            url=f"postgresql+psycopg://{self.config.user}:{self.config.password}"
                f"@{self.config.host}:{self.config.port}/{self.config.name}",
            echo=False
        )
        self.session_factory = sessionmaker(self.engine)

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(primary_key=True)
    hashed_password: Mapped[str]
    telegram: Mapped[str]
    token: Mapped[str] = mapped_column(nullable=True)

from sqlalchemy.orm import sessionmaker
from config import load_database_config
from database.models import Base, User
from sqlalchemy import select, create_engine, update


class Database:
    def __init__(self):
        self.config = load_database_config()
        self.engine = create_engine(
            url=f"postgresql+psycopg://{self.config.user}:{self.config.password}"
                f"@{self.config.host}:{self.config.port}/{self.config.name}",
            echo=False
        )
        self.session_factory = sessionmaker(self.engine)

    def create_tables(self) -> None:
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def get_user_data(self, email: str = None, user_agent: str = False) -> User:
        with self.session_factory() as session:
            if user_agent:
                select_user_query = select(User).where(User.user_agent == user_agent)
                result = session.execute(select_user_query).scalar()
            else:
                select_user_query = select(User).where(User.email == email)
                result = session.execute(select_user_query).scalar()
        return result

    def create_user(self, email: str, password: str, telegram: str, user_agent: str) -> None:
        with self.session_factory() as session:
            user = User(
                email=email,
                hashed_password=password,
                telegram=telegram,
                user_agent=user_agent
            )
            session.add(user)
            session.flush()
            session.commit()

    def update_user_token(self, new_token: str, email: str) -> None:
        with self.session_factory() as session:
            query = update(
                User
            ).values(
                {'token': new_token}
            ).filter_by(
                email=email
            )
            session.execute(query)
            session.commit()

    def __call__(self):
        self.create_tables()

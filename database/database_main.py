from database.models import DatabaseConnect, Base, User
from sqlalchemy import select


class Database(DatabaseConnect):
    def create_tables(self) -> None:
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def check_user_in_base(self, email: str, get_user: bool = False) -> bool | User:
        with self.session_factory() as session:
            if get_user:
                select_user_query = select(User).where(User.email == email)
                result = session.execute(select_user_query).scalar()
            else:
                select_user_query = select(1).where(User.email == email)
                result = session.execute(select_user_query).scalar()
        return result

    def __call__(self):
        self.create_tables()

    def create_user(self, email: str, password: str, telegram: str) -> None:
        with self.session_factory() as session:
            user = User(
                email=email,
                hashed_password=password,
                telegram=telegram
            )
            session.add(user)
            session.flush()
            session.commit()

    def select_all_users(self) -> list[User]:
        with self.session_factory() as session:
            query = select(User)
            result = session.execute(query)
            users = result.scalars().all()
            return users

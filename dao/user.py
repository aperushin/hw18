from .model.models import User
from sqlalchemy.exc import NoResultFound


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self) -> list[User]:
        query = self.session.query(User)
        return query.all()

    def get_by_id(self, uid: int) -> User:
        query = self.session.query(User)
        return query.get(uid)

    def get_by_username(self, username: str) -> User | None:
        try:
            user = self.session.query(User).filter_by(username=username).one()
        except NoResultFound:
            return None
        return user

    def add(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, uid: int, user_data: dict):
        self.session.query(User).filter_by(id=uid).update(user_data)
        self.session.commit()

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()

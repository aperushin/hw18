import base64
import hashlib
import hmac

from dao.user import UserDAO
from dao.model.models import User, UserSchema
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, HASH_ALGORYTHM


class UserService:

    def __init__(self, users_dao: UserDAO):
        self.users_dao: UserDAO = users_dao

    @staticmethod
    def _validate(user_data) -> dict:
        validated_data = UserSchema().load(user_data)
        return validated_data

    def generate_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            HASH_ALGORYTHM,
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )).decode('utf-8', 'ignore')

    def compare_passwords(self, password: str, password_hash: str):
        other_password_hash = self.generate_hash(password)
        return hmac.compare_digest(password_hash, other_password_hash)

    def get_all(self) -> list[User]:
        return self.users_dao.get_all()

    def get_by_id(self, uid):
        return self.users_dao.get_by_id(uid)

    def get_by_username(self, username: str) -> User | None:
        return self.users_dao.get_by_username(username)

    def create(self, user_data: dict) -> User:
        user_data = self._validate(user_data)
        user_data['password'] = self.generate_hash(user_data['password'])
        new_user = User(**user_data)
        user_added = self.users_dao.add(new_user)
        return user_added

    def update(self, uid: int, user_data: dict) -> bool:
        user: User = self.users_dao.get_by_id(uid)
        if not user:
            return False

        new_user_data = self._validate(user_data)
        new_user_data['password'] = self.generate_hash(new_user_data['password'])
        self.users_dao.update(uid, new_user_data)
        return True

    def delete(self, uid: int) -> bool:
        user = self.users_dao.get_by_id(uid)
        if not user:
            return False

        self.users_dao.delete(user)
        return True

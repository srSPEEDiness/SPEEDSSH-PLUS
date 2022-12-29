import datetime
from typing import List
from checkuser.data.driver import Driver
from checkuser.domain.user import User
from checkuser.domain.repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, driver: Driver):
        self.driver = driver

    def get_by_username(self, username: str) -> User:
        user_id = self.driver.get_id(username)
        expiration_date = self.driver.get_expiration_date(username)
        connection_limit = self.driver.get_connection_limit(username)
        return User(user_id, username, expiration_date, connection_limit)

    def get_all(self) -> List[User]:
        users = self.driver.get_users()
        return [self.get_by_username(user) for user in users]


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = [
            User(1000, 'user1', datetime.datetime(2023, 1, 1), 10),
            User(1002, 'user2', datetime.datetime(2023, 1, 1), 10),
        ]

    def get_by_username(self, username: str) -> User:
        try:
            return next(user for user in self.users if user.username == username)
        except StopIteration:
            raise ValueError('User not found')

    def get_all(self) -> List[User]:
        return self.users

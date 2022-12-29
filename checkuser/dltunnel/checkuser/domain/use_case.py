import datetime

from typing import Union, NamedTuple, List
from checkuser.domain.connection import Connection, ConnectionKill
from checkuser.domain.repository import UserRepository


class OutputDTO(NamedTuple):
    id: int
    username: str
    expiration_date: Union[None, datetime.datetime]
    limit_connections: int
    count_connections: int


class CheckUserUseCase:
    def __init__(self, repository: UserRepository, connections: List[Connection]) -> None:
        self.repository = repository
        self.connections = connections

    def execute(self, username: str) -> OutputDTO:
        user = self.repository.get_by_username(username)
        count = sum([connection.count(username) for connection in self.connections])
        return OutputDTO(
            id=user.id,
            username=user.username,
            expiration_date=user.expiration_date,
            limit_connections=user.connection_limit,
            count_connections=count,
        )


class KillConnectionUseCase:
    def __init__(self, connections: List[ConnectionKill]) -> None:
        self.connections = connections

    def execute(self, username: str) -> None:
        for connection in self.connections:
            connection.kill(username)


class AllConnectionsUseCase:
    def __init__(self, connections: List[Connection]) -> None:
        self.connections = connections

    def execute(self) -> int:
        return sum([connection.all() for connection in self.connections])

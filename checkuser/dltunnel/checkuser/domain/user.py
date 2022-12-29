from typing import NamedTuple, Union
from datetime import datetime


class User(NamedTuple):
    id: int
    username: str
    expiration_date: Union[datetime, None]
    connection_limit: int

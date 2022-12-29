from abc import ABCMeta, abstractmethod
from typing import NamedTuple


class HttpRequest(NamedTuple):
    query: dict
    body: dict


class HttpResponse(NamedTuple):
    status_code: int
    body: dict


class Controller(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse:
        raise NotImplementedError()

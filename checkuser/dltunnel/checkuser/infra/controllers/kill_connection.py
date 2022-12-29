from checkuser.domain.use_case import KillConnectionUseCase
from ..controller import Controller, HttpRequest, HttpResponse


class KillConnectionController(Controller):
    def __init__(self, use_case: KillConnectionUseCase) -> None:
        self.use_case = use_case

    def handle(self, request: HttpRequest) -> HttpResponse:
        self.use_case.execute(request.query['username'])
        return HttpResponse(status_code=204, body={})

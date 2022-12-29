from unittest.mock import Mock
from datetime import datetime, timedelta


from checkuser.domain.user import User
from checkuser.domain.use_case import CheckUserUseCase, KillConnectionUseCase
from checkuser.infra.controller import HttpRequest
from checkuser.infra.controllers.check_user import CheckUserController
from checkuser.infra.controllers.kill_connection import KillConnectionController


def test_should_check_user():
    repository = Mock()
    repository.get_by_username.return_value = User(
        id=1000,
        username='test',
        expiration_date=datetime.now() + timedelta(days=10),
        connection_limit=10,
    )

    connection = Mock()
    connection.count.return_value = 5

    use_case = CheckUserUseCase(repository, [connection])
    controller = CheckUserController(use_case)
    response = controller.handle(
        HttpRequest(
            query={'username': 'test'},
            body={},
        )
    )

    assert response.status_code == 200
    assert response.body['id'] == 1000


def test_should_kill_connection():
    connection = Mock()
    connection.kill.return_value = None

    use_case = KillConnectionUseCase([connection])
    controller = KillConnectionController(use_case)

    controller.handle(HttpRequest(query={'username': 'test'}, body={}))
    connection.kill.assert_called_once_with('test')

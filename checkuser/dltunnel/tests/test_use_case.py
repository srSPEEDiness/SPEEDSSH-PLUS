from unittest.mock import Mock

from checkuser.domain.user import User
from checkuser.domain.use_case import CheckUserUseCase


def test_should_check_user():
    repository = Mock()
    repository.get_by_username.return_value = User(
        id=1000,
        username='test',
        expiration_date=None,
        connection_limit=10,
    )

    connection_count = Mock()
    connection_count.count.return_value = 5

    use_case = CheckUserUseCase(repository, [connection_count])
    output_dto = use_case.execute('test')

    assert output_dto.id == 1000

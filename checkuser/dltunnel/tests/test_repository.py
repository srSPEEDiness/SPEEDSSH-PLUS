from unittest.mock import Mock
from datetime import datetime, timedelta
from checkuser.data.driver import FormatDateUS

from checkuser.data.executor import CommandExecutorImpl
from checkuser.data.repository import UserRepositoryImpl


def test_should_get_user_by_username():
    username = 'test'

    executor = CommandExecutorImpl()
    format_date = FormatDateUS()
    # driver = DriverImpl(executor, format_date)
    driver = Mock()
    driver.get_id.return_value = 1000
    driver.get_expiration_date.return_value = datetime.now() + timedelta(days=1)
    driver.get_connection_limit.return_value = 0
    driver.get_users.return_value = [username]

    repository = UserRepositoryImpl(driver)

    user = repository.get_by_username(username)
    assert user.id == 1000
    assert user.username == username
    assert user.expiration_date is not None
    assert user.connection_limit == 0

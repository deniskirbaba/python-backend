from datetime import datetime

import pytest
from pydantic import SecretStr

from lecture_4.demo_service.core.users import (
    UserEntity,
    UserInfo,
    UserRole,
    UserService,
    password_is_longer_than_8,
)


@pytest.fixture(scope="module")
def user_service() -> UserService:
    return UserService([password_is_longer_than_8])


@pytest.mark.parametrize(
    "username, password, error",
    [
        ("hunter7", "short", True),
        ("maximus", "ksdaflkjasdf", False),
        ("maximus", "lsdakfjasdf", True),
    ],
)
def test_register(user_service, username: str, password: str, error: bool):
    user_info = UserInfo(
        username=username,
        name="name",
        birthdate=datetime.now(),
        password=SecretStr(password),
    )
    if error:
        with pytest.raises(ValueError):
            user_service.register(user_info)
    else:
        user_entity = user_service.register(user_info)
        assert isinstance(user_entity, UserEntity)


def test_get(user_service):
    # get_by_username
    assert isinstance(user_service.get_by_username("maximus"), UserEntity)
    assert user_service.get_by_username("qqq") is None

    # get_by_id
    assert isinstance(user_service.get_by_id(1), UserEntity)
    assert user_service.get_by_username(10) is None


def test_grant_admin(user_service):
    user_service.grant_admin(1)
    assert user_service.get_by_id(1).info.role == UserRole.ADMIN

    with pytest.raises(ValueError):
        user_service.grant_admin(10)

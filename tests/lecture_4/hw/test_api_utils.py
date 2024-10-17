from datetime import datetime
from http import HTTPStatus

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI, HTTPException, Request
from fastapi.security import HTTPBasicCredentials
from httpx import ASGITransport, AsyncClient
from pydantic import SecretStr

from lecture_4.demo_service.api.utils import (
    initialize,
    requires_admin,
    requires_author,
    user_service,
    value_error_handler,
)
from lecture_4.demo_service.core.users import (
    UserEntity,
    UserInfo,
    UserRole,
)


@pytest_asyncio.fixture(scope="module")
async def app():
    app = FastAPI(lifespan=initialize)
    return app


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, authorized",
    [
        ("admin", "superSecretAdminPassword123", True),
        ("admin", "wrong_password", False),
        ("not_even_admin", "also_wring_password", False),
    ],
)
async def test_authorization(app, username: str, password: str, authorized: bool):
    async with LifespanManager(app) as manager:
        async with AsyncClient(transport=ASGITransport(app=manager.app)):
            request = Request(scope={"type": "http", "app": app})
            service = user_service(request)
            credentials = HTTPBasicCredentials(username=username, password=password)
            if not authorized:
                with pytest.raises(HTTPException):
                    requires_author(credentials=credentials, user_service=service)
            else:
                user_entity = requires_author(
                    credentials=credentials, user_service=service
                )
                assert isinstance(user_entity, UserEntity)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, role",
    [
        ("hunter", "alsdkjfhsdaf78", UserRole.ADMIN),
        ("doctor", "saiuh34lkjsafgsd;jkl", UserRole.USER),
    ],
)
async def test_admin(app, username: str, password: str, role: UserRole):
    async with LifespanManager(app) as manager:
        async with AsyncClient(transport=ASGITransport(app=manager.app)):
            request = Request(scope={"type": "http", "app": app})
            service = user_service(request)
            user_entity = service.register(
                UserInfo(
                    username=username,
                    name="name",
                    birthdate=datetime.now(),
                    role=role,
                    password=SecretStr(password),
                )
            )

            if role == UserRole.USER:
                with pytest.raises(HTTPException):
                    requires_admin(user_entity)
            else:
                user_entity = requires_admin(user_entity)
                assert isinstance(user_entity, UserEntity)


@pytest.mark.asyncio
async def test_value_error_handler():
    request = Request(scope={"type": "http", "method": "GET", "path": "/fake_path"})
    response = await value_error_handler(request, ValueError("Fake path error"))
    assert response.status_code == HTTPStatus.BAD_REQUEST

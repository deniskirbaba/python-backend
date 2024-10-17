from datetime import datetime
from http import HTTPStatus

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from lecture_4.demo_service.api.main import create_app
from lecture_4.demo_service.api.utils import (
    requires_admin,
    requires_author,
)
from lecture_4.demo_service.core.users import (
    UserRole,
)


@pytest.fixture()
def app() -> FastAPI:
    app = create_app()
    return app


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, status",
    [
        ("jack37", "s;lkjrfstshguhtd787dgt9", HTTPStatus.OK),
        ("wolf13", "dflksdjfdskldsf", HTTPStatus.BAD_REQUEST),
        ("admin", "dflksd24jfdskldsf", HTTPStatus.BAD_REQUEST),
        ("ronaldo7", "asdf24", HTTPStatus.BAD_REQUEST),
    ],
)
async def test_register(
    app: FastAPI, username: str, password: str, status: HTTPStatus
) -> None:
    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app), base_url="http://127.0.0.1:8000"
        ) as client:
            request_json = {
                "username": username,
                "name": "name",
                "birthdate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "password": password,
            }
            response = await client.post("/user-register", json=request_json)
            assert response.status_code == status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "id, username, status",
    [
        (35, "asdftdjgk", HTTPStatus.BAD_REQUEST),
        (None, None, HTTPStatus.BAD_REQUEST),
        (1, None, HTTPStatus.OK),
        (None, "admin", HTTPStatus.OK),
        (124, None, HTTPStatus.NOT_FOUND),
    ],
)
async def test_get(
    app: FastAPI, id: int | None, username: str | None, status: HTTPStatus
):
    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app), base_url="http://127.0.0.1:8000"
        ) as client:
            if id is not None and username is not None:
                app.dependency_overrides[requires_author] = lambda: None
                response = await client.post(
                    "/user-get", params={"id": id, "username": username}
                )
            elif id is None and username is None:
                app.dependency_overrides[requires_author] = lambda: None
                response = await client.post("/user-get")
            elif id is not None:
                app.dependency_overrides[requires_author] = (
                    lambda: app.state.user_service.get_by_id(1)
                )
                response = await client.post("/user-get", params={"id": id})
            elif username is not None:
                app.dependency_overrides[requires_author] = (
                    lambda: app.state.user_service.get_by_username(username)
                )
                response = await client.post("/user-get", params={"username": username})

            assert response.status_code == status


@pytest.mark.asyncio
async def test_promote(app: FastAPI):
    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app), base_url="http://127.0.0.1:8000"
        ) as client:
            app.dependency_overrides[requires_admin] = lambda: None
            request_json = {
                "username": "username",
                "name": "name",
                "birthdate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "password": "sdfldsaf35353",
            }
            register_response = await client.post("/user-register", json=request_json)
            assert register_response.status_code == HTTPStatus.OK

            promotion_response = await client.post("/user-promote", params={"id": 2})
            assert promotion_response.status_code == HTTPStatus.OK

            user_entity = app.state.user_service.get_by_id(2)
            assert user_entity.info.role == UserRole.ADMIN

import math
from http import HTTPStatus
from typing import Any

import pytest
from async_asgi_testclient import TestClient
from lecture_1.math_api.app import app


def calculate_fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("GET", "/"),
        ("GET", "/not_found"),
        ("POST", "/"),
        ("PUT", "/not_found"),
    ],
)
async def test_not_found(method: str, path: str):
    async with TestClient(app) as client:
        response = await client.open(
            path,
            method=method,
        )
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("query", "status_code", "expected_result"),
    [
        ({"n": ""}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ({"n": "lol"}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ({"x": "kek"}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ({}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ({"n": -1}, HTTPStatus.BAD_REQUEST, None),
        ({"n": 0}, HTTPStatus.OK, 1),
        ({"n": 1}, HTTPStatus.OK, 1),
        ({"n": 5}, HTTPStatus.OK, 120),
        ({"n": 10}, HTTPStatus.OK, 3628800),
        ({"n": 1001}, HTTPStatus.BAD_REQUEST, None),  # Beyond MAX_FACTORIAL_N
    ],
)
async def test_factorial(query: dict[str, Any], status_code: int, expected_result: Any):
    async with TestClient(app) as client:
        response = await client.get("/factorial", query_string=query)

    assert response.status_code == status_code
    if status_code == HTTPStatus.OK:
        result = response.json().get("result")
        assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("params", "status_code", "expected_result"),
    [
        ("/", HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ("/lol", HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ("/-1", HTTPStatus.BAD_REQUEST, None),
        ("/0", HTTPStatus.OK, 0),
        ("/1", HTTPStatus.OK, 1),
        ("/5", HTTPStatus.OK, 5),
        ("/10", HTTPStatus.OK, 55),
        ("/15", HTTPStatus.OK, 610),
        ("/10001", HTTPStatus.BAD_REQUEST, None),  # Beyond MAX_FIBONACCI_N
    ],
)
async def test_fibonacci(params: str, status_code: int, expected_result: Any):
    async with TestClient(app) as client:
        response = await client.get("/fibonacci" + params)

    assert response.status_code == status_code
    if status_code == HTTPStatus.OK:
        result = response.json().get("result")
        assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("json", "status_code", "expected_result"),
    [
        (None, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ([1, "two", 3], HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ("hello", HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ([], HTTPStatus.BAD_REQUEST, None),
        ([1, 2, 3], HTTPStatus.OK, 2.0),
        ([1, 2.0, 3.0], HTTPStatus.OK, 2.0),
        ([1.0, 2.0, 3.0], HTTPStatus.OK, 2.0),
        ([1, 2, 3, 4, 5], HTTPStatus.OK, 3.0),
    ],
)
async def test_mean(
    json: dict[str, Any] | None, status_code: int, expected_result: Any
):
    async with TestClient(app) as client:
        response = await client.get("/mean", json=json)

    assert response.status_code == status_code
    if status_code == HTTPStatus.OK:
        result = response.json().get("result")
        assert math.isclose(result, expected_result, rel_tol=1e-9)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("headers", "json", "status_code"),
    [
        ({"Content-Type": "application/json"}, [1, 2, 3], HTTPStatus.OK),
        ({"Content-Type": "text/plain"}, [1, 2, 3], HTTPStatus.OK),
        (
            {"Content-Type": "application/json"},
            "not-a-list",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
async def test_mean_content_type(headers: dict[str, str], json: Any, status_code: int):
    async with TestClient(app) as client:
        response = await client.get("/mean", json=json, headers=headers)

    assert response.status_code == status_code
    if status_code == HTTPStatus.OK:
        assert "result" in response.json()


@pytest.mark.asyncio
async def test_unsupported_method():
    async with TestClient(app) as client:
        response = await client.post("/factorial", json={"n": 5})
    assert response.status_code == HTTPStatus.NOT_FOUND

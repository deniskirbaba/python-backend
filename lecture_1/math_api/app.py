import json
from http import HTTPMethod, HTTPStatus
from typing import Any, Awaitable, Callable

from lecture_1.math_api.routes import (
    handle_factorial_request,
    handle_fibonacci_request,
    handle_mean_request,
)
from lecture_1.math_api.utils import read_body


async def app(
    scope: dict[str, Any],
    receive: Callable[[], Awaitable[dict[str, Any]]],
    send: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:

    method = scope.get("method")
    path = scope.get("path")
    query_string = scope.get("query_string", b"").decode("utf-8")

    status = HTTPStatus.NOT_FOUND
    response_body = {"error": "Not Found"}

    if method == HTTPMethod.GET:
        if path == "/factorial":
            status, response_body = handle_factorial_request(query_string)
        elif path.startswith("/fibonacci/"):
            path_params = path.split("/")[2:]
            status, response_body = handle_fibonacci_request(path_params)
        elif path == "/mean":
            body = await read_body(receive)
            status, response_body = handle_mean_request(body.decode("utf-8"))

    await send(
        {
            "type": "http.response.start",
            "status": status.value,
            "headers": [[b"content-type", b"application/json"]],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": json.dumps(response_body).encode("utf-8"),
        }
    )

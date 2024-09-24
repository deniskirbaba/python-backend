import json
from http import HTTPMethod
from http import HTTPStatus
from typing import Any
from typing import Awaitable
from typing import Callable

import uvicorn

from math_api.routes import handle_factorial_request
from math_api.routes import handle_fibonacci_request
from math_api.routes import handle_mean_request
from math_api.utils import read_body


async def application(
    scope: dict[str, Any],
    receive: Callable[[], Awaitable[dict[str, Any]]],
    send: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:
    assert scope["type"] == "http"

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
        {"type": "http.response.start", "status": status.value, "headers": [[b"content-type", b"application/json"]]}
    )
    await send({"type": "http.response.body", "body": json.dumps(response_body).encode("utf-8")})


def main() -> None:
    uvicorn.run("math_api.app:application", port=8000, log_level="info")


if __name__ == "__main__":
    main()

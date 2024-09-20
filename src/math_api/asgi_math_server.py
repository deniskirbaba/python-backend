import json
from http import HTTPMethod
from http import HTTPStatus
from math import factorial as math_factorial
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Optional
from typing import Tuple
from typing import Union

import uvicorn


# Utility function to check if a string represents an integer
def represents_int(s: Any) -> bool:
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False


def handle_factorial_request(query: str) -> Tuple[HTTPStatus, Optional[Union[dict[str, int], dict[str, str]]]]:
    query_params = {param.split("=")[0]: param.split("=")[1] for param in query.split("&") if "=" in param}
    n = query_params.get("n")

    # Validation
    if n is None:
        return (HTTPStatus.UNPROCESSABLE_ENTITY, {"error": "Missing parameter 'n'"})
    if not represents_int(n):
        return (HTTPStatus.UNPROCESSABLE_ENTITY, {"error": "'n' must be an integer"})
    n = int(n)
    if n < 0:
        return (HTTPStatus.BAD_REQUEST, {"error": "'n' must be a non-negative integer"})

    try:
        result = math_factorial(n)
        return (HTTPStatus.OK, {"result": result})
    except ValueError:
        return (HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Internal server error during factorial computation"})


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

    # Routing logic
    if method == HTTPMethod.GET:
        if path == "/factorial":
            status, response_body = handle_factorial_request(query_string)
        elif path == "/fibonacci":
            status, response_body = HTTPStatus.NOT_IMPLEMENTED, {"error": "Not implemented"}
        elif path == "/mean":
            status, response_body = HTTPStatus.NOT_IMPLEMENTED, {"error": "Not implemented"}
    else:
        response_body = {"error": f"Method {method} not allowed"}

    await send(
        {"type": "http.response.start", "status": status.value, "headers": [[b"content-type", b"application/json"]]}
    )
    await send({"type": "http.response.body", "body": json.dumps(response_body).encode("utf-8")})


def main():
    uvicorn.run("math_api.asgi_math_server:application", port=8000, log_level="info")


if __name__ == "__main__":
    main()


def fibonacci():
    pass


def mean():
    pass

import json
from functools import lru_cache
from http import HTTPMethod
from http import HTTPStatus
from math import factorial as math_factorial
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from urllib.parse import parse_qs

import uvicorn

MAX_FACTORIAL_N = 1e3
MAX_FIBONACCI_N = 1e4


def validate_int_param(param: List, param_name: str) -> Tuple[Optional[int], HTTPStatus, Optional[dict[str, str]]]:
    if len(param) != 1:
        return None, HTTPStatus.UNPROCESSABLE_ENTITY, {"error": f"Missing parameter '{param_name}'"}
    try:
        n = int(param[0])
    except (ValueError, TypeError):
        return None, HTTPStatus.UNPROCESSABLE_ENTITY, {"error": f"'{param_name}' must be an integer"}
    if n < 0:
        return None, HTTPStatus.BAD_REQUEST, {"error": f"'{param_name}' must be a non-negative integer"}
    return n, HTTPStatus.OK, None


def handle_factorial_request(query: str) -> Tuple[HTTPStatus, dict[str, Union[int, str]]]:
    query_params = parse_qs(query)
    n, status, error_response = validate_int_param(query_params.get("n", []), "n")

    if error_response:
        return status, error_response

    if n > MAX_FACTORIAL_N:
        return HTTPStatus.BAD_REQUEST, {"error": f"'n' must be less than or equal to {MAX_FACTORIAL_N}"}

    try:
        result = math_factorial(n)
        return HTTPStatus.OK, {"result": result}
    except Exception as e:
        return HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"Internal error during factorial computation: {str(e)}"}


@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b

    return b


def handle_fibonacci_request(path_params: List[str]) -> Tuple[HTTPStatus, dict[str, Union[int, str]]]:
    n, status, error_response = validate_int_param(path_params, "n")

    if error_response:
        return status, error_response

    if n > MAX_FIBONACCI_N:
        return HTTPStatus.BAD_REQUEST, {"error": f"'n' must be less than or equal to {MAX_FIBONACCI_N}"}

    try:
        result = fibonacci(n)
        return HTTPStatus.OK, {"result": result}
    except Exception as e:
        return HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"Internal error during Fibonacci computation: {str(e)}"}


async def read_body(receive):
    body = b""
    more_body = True

    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)

    return body


def handle_mean_request(data: str) -> Tuple[HTTPStatus, dict[str, Union[float, str]]]:
    try:
        float_list = json.loads(data)
        if not isinstance(float_list, list) or not all(isinstance(i, (float, int)) for i in float_list):
            return HTTPStatus.UNPROCESSABLE_ENTITY, {"error": "Passed array does not contain a valid list of floats"}
    except json.JSONDecodeError:
        return HTTPStatus.UNPROCESSABLE_ENTITY, {"error": "Invalid type of passed array"}

    if len(float_list) == 0:
        return HTTPStatus.BAD_REQUEST, {"error": "Passed array should be non-empty"}

    result = sum(float_list) / len(float_list)
    return HTTPStatus.OK, {"result": result}


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


def main():
    uvicorn.run("math_api.asgi_math_server:application", port=8000, log_level="info")


if __name__ == "__main__":
    main()

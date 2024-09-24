from math import factorial as math_factorial
from http import HTTPStatus
from functools import lru_cache
import json

MAX_FACTORIAL_N = 1e3
MAX_FIBONACCI_N = 1e4

def factorial_service(n: int):
    if n > MAX_FACTORIAL_N:
        return HTTPStatus.BAD_REQUEST, {"error": f"'n' must be less than or equal to {MAX_FACTORIAL_N}"}
    try:
        result = math_factorial(n)
        return HTTPStatus.OK, {"result": result}
    except Exception as e:
        return HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"Internal error during factorial computation: {str(e)}"}

@lru_cache(maxsize=None)
def fibonacci_service(n: int):
    if n > MAX_FIBONACCI_N:
        return HTTPStatus.BAD_REQUEST, {"error": f"'n' must be less than or equal to {MAX_FIBONACCI_N}"}
    try:
        if n == 0:
            return HTTPStatus.OK, {"result": 0}
        elif n == 1:
            return HTTPStatus.OK, {"result": 1}

        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b

        return HTTPStatus.OK, {"result": b}
    except Exception as e:
        return HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"Internal error during Fibonacci computation: {str(e)}"}

def mean_service(data: str):
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

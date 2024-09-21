from functools import lru_cache
from http import HTTPStatus
from math import factorial
from typing import Annotated

import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get(
    "/factorial",
    summary="Calculate the factorial of a number",
    description="This endpoint calculates the factorial of a non-negative integer n.",
)
def get_factorial(n: Annotated[int, Query(..., ge=0, description="A non-negative integer")]) -> JSONResponse:
    result = factorial(n)
    return JSONResponse({"result": result})


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


@app.get(
    "/fibonacci/{n}",
    summary="Get the nth Fibonacci number",
    description="Returns the nth Fibonacci number for a non-negative integer n.",
)
def get_fibonacci(n: int) -> JSONResponse:
    if n < 0:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid value for 'n', must be non-negative")
    result = fibonacci(n)
    return JSONResponse({"result": result})


@app.get(
    "/mean",
    summary="Calculate the mean of a list of numbers",
    description="This endpoint calculates the mean of a non-empty list of floats.",
)
def get_mean(data: list[float]):
    if len(data) == 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid value for body, must be non-empty array of floats"
        )
    result = sum(data) / len(data)
    return JSONResponse({"result": result})


def main():
    uvicorn.run("fast_api_server:app", port=8000, log_level="info")


if __name__ == "__main__":
    main()

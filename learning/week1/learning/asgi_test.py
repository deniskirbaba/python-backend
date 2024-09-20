import uvicorn
from typing import Any, Awaitable, Callable


async def application(
    scope: dict[str, Any],
    receive: Callable[[], Awaitable[dict[str, Any]]],
    send: Callable[[dict[str, Any]], Awaitable[None]]
) -> None:
    assert scope['type'] == 'http'
    
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/plain"],
            ],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": b"Hello, world!"
        }
    )

if __name__ == "__main__":
    uvicorn.run("asgi_test:application", port=8000, log_level="info")
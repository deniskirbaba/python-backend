from typing import List, Tuple, Optional
from http import HTTPStatus

async def read_body(receive):
    body = b""
    more_body = True
    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)
    return body

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

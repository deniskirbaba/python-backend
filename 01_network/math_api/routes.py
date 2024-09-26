from urllib.parse import parse_qs

from math_api.services import factorial_service, fibonacci_service, mean_service
from math_api.utils import validate_int_param


def handle_factorial_request(query: str):
    query_params = parse_qs(query)
    n, status, error_response = validate_int_param(query_params.get("n", []), "n")

    if error_response:
        return status, error_response
    return factorial_service(n)


def handle_fibonacci_request(path_params):
    n, status, error_response = validate_int_param(path_params, "n")

    if error_response:
        return status, error_response
    return fibonacci_service(n)


def handle_mean_request(data):
    return mean_service(data)

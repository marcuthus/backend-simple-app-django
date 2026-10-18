from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Standardized custom exception handler for Django REST Framework.
    Returns:
    {
        "status_code": 400,
        "error": "Bad Request",
        "detail": ...
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        data = {
            'status_code': response.status_code,
            'error': response.status_text,
            'detail': response.data
        }
        response.data = data

    return response

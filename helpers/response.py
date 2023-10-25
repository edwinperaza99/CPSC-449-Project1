from fastapi import HTTPException
from models import Response

def create_response(status_code: int, message: str, *data: list | dict) -> Response:
    return Response(status=status_code, message=message, data=data or None)

def raise_exception(status_code: int, message: str):
    raise HTTPException(status_code=status_code, detail = message)
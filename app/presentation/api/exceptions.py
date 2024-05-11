from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.domain.exceptions.access import AccessDeniedError, AuthenticationError


class ApiError(BaseModel):
    detail: str | dict[str, Any]


def authentication_error_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        ApiError(detail="Incorrect username or password"),
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )


def access_denied_error_handler(request: Request, exc: AccessDeniedError):
    return JSONResponse(
        ApiError(detail="You don't have access to do this"),
        status_code=status.HTTP_403_FORBIDDEN,
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AuthenticationError, authentication_error_handler)
    app.add_exception_handler(AccessDeniedError, access_denied_error_handler)

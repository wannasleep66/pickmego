from collections.abc import Awaitable, Callable

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler

from common.error import (
    AppError,
    EntityConflictError,
    EntityNotFoundError,
    UnauthorizedError,
    ValidationError,
)


def error_handler(
    status_code: int,
) -> Callable[[Request, AppError], Awaitable[Response]]:
    async def handler(request: Request, exc: AppError) -> Response:
        return await http_exception_handler(
            request,
            HTTPException(status_code=status_code, detail=[exc.schema.model_dump()]),
        )

    return handler


def use_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(EntityNotFoundError)(error_handler(status.HTTP_404_NOT_FOUND))
    app.exception_handler(EntityConflictError)(error_handler(status.HTTP_409_CONFLICT))
    app.exception_handler(PermissionError)(error_handler(status.HTTP_403_FORBIDDEN))
    app.exception_handler(UnauthorizedError)(
        error_handler(status.HTTP_401_UNAUTHORIZED)
    )
    app.exception_handler(ValidationError)(error_handler(status.HTTP_422_UNPROCESSABLE_CONTENT))

from abc import abstractmethod
from typing import Self

from pydantic import BaseModel

from common.http.schemas.error import ErrorSchema, ValidationErrorSchema


class AppError(Exception):
    @property
    def type(self: Self) -> str:
        return type(self).__name__.replace("Error", "")

    @property
    @abstractmethod
    def msg(self: Self) -> str: ...

    @property
    def schema(self: Self) -> BaseModel:
        return ErrorSchema(type=self.type, msg=self.msg)


class EntityNotFoundError(AppError):
    def __init__(self, entity: str) -> None:
        self.entity = entity
        super().__init__()

    @property
    def msg(self: Self) -> str:
        return f"Не удалось найти {self.entity}"


class EntityConflictError(AppError):
    def __init__(self, entity: str, action: str) -> None:
        self.entity = entity
        self.action = action
        super().__init__()

    @property
    def msg(self: Self) -> str:
        return f"Конфликт при попытке {self.action} {self.entity}"


class PermissionError(AppError):
    def __init__(self, action: str, entity: str) -> None:
        self.action = action
        self.entity = entity
        super().__init__()

    @property
    def msg(self: Self) -> str:
        return f"Недостаточно прав для {self.action} {self.entity}"


class UnauthorizedError(AppError):
    @property
    def msg(self: Self) -> str:
        return "Не авторизован"


class ValidationError(AppError):
    def __init__(self, fields: dict[str, str]) -> None:
        self.fields = fields
        super().__init__()

    @property
    def msg(self: Self) -> str:
        return "Некорректные данные"

    @property
    def schema(self: Self) -> BaseModel:
        return ValidationErrorSchema(
            type=self.type,
            msg=self.msg,
            fields=self.fields
        )

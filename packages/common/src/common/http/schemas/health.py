from typing import Literal

from common.http.schemas.base import ResponseSchema


class HealthResponseSchema(ResponseSchema):
    status: Literal["ok", "error"]

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    type: str
    msg: str


class ValidationErrorSchema(ErrorSchema):
    fields: dict[str, str]

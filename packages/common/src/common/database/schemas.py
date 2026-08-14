from pydantic import BaseModel


class CreateSchema(BaseModel): ...


class ReadSchema(BaseModel):
    id: int


class UpdateSchema(BaseModel): ...

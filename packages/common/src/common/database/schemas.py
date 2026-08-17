from pydantic import BaseModel, ConfigDict


class CreateSchema(BaseModel): ...


class ReadSchema(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UpdateSchema(BaseModel): ...

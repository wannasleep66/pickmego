from typing import Any, Self, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import Base
from common.database.schemas import CreateSchema, ReadSchema, UpdateSchema

Model = TypeVar("Model", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=CreateSchema)
ReadSchemaType = TypeVar("ReadSchemaType", bound=ReadSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=UpdateSchema)


class DatabaseRepository[Model, CreateSchemaType, ReadSchemaType, UpdateSchemaType]:
    model: type[Model]
    schema: ReadSchemaType

    def __init__(self: Self, session: AsyncSession) -> None:
        self.session = session

    async def get(self: Self, id_: int) -> ReadSchemaType | None:
        query = select(self.model).filter_by(id=id_)
        instance = await self.session.scalar(query)
        return self.schema.model_validate(instance) if instance else None

    async def get_by(self: Self, **condition: Any) -> ReadSchemaType | None:
        query = select(self.model).filter_by(**condition)
        instance = await self.session.scalar(query)
        return self.schema.model_validate(instance) if instance else None

    async def get_by_ids(self: Self, ids: list[int]) -> list[ReadSchemaType]:
        query = select(self.model).filter(self.model.id.in_(ids))
        instances = await self.session.scalars(query)
        return [self.schema.model_validate(instance) for instance in instances]

    async def get_all(self: Self) -> list[ReadSchemaType]:
        query = select(self.model)
        instances = await self.session.scalars(query)
        return [self.schema.model_validate(instance) for instance in instances]

    async def create(self: Self, data: CreateSchemaType) -> ReadSchemaType:
        stmt = insert(self.model).values(data.model_dump()).returning(self.model)
        instance = await self.session.scalar(stmt)
        return self.schema.model_validate(instance)

    async def update(self: Self, id_: int, data: UpdateSchemaType) -> ReadSchemaType:
        stmt = update(self.model).filter_by(id=id_).values(**data.model_dump()).returning(self.model)
        instance = await self.session.scalar(stmt)
        return self.schema.model_validate(instance)

    async def bulk_update(self: Self, **condition: Any, data: UpdateSchemaType) -> list[ReadSchemaType]:
        stmt = update(self.model).filter_by(**condition).values(**data.model_dump())
        instances = await self.session.scalars(stmt)
        return [self.schema.model_validate(instance) for instance in instances]

    async def delete(self: Self, id_: int) -> None:
        stmt = delete(self.model).filter_by(id=id_)
        await self.session.execute(stmt)

    async def delete_by_ids(self: Self, ids: list[int]) -> None:
        stmt = delete(self.model).filter(self.model.id.in_(ids))
        await self.session.execute(stmt)

    async def bulk_delete(self: Self, **condition: Any) -> None:
        stmt = delete(self.model).filter_by(**condition)
        await self.session.execute(stmt)

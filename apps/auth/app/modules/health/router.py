from common.http.schemas.health import HealthResponseSchema
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from redis.asyncio import Redis, RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/")
@inject
async def health(database: FromDishka[AsyncSession], cache: FromDishka[Redis]) -> HealthResponseSchema:
    try:
        await database.execute(text("SELECT VERSION()"))
        await cache.ping()

        return HealthResponseSchema(status="ok")
    except (SQLAlchemyError, RedisError):
        return HealthResponseSchema(status="error")

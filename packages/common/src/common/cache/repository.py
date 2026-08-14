from typing import Self

from redis.asyncio import Redis


class CacheRepository:
    def __init__(self: Self, client: Redis) -> None:
       self.client = client

    async def set(self: Self, key: str, value: str) -> None:
       await self.client.set(key, value)

    async def get(self: Self, key: str) -> str | None:
       value = await self.client.get(key)

       if isinstance(value, bytes):
           return value.decode()

       return value

    async def delete(self: Self, key: str) -> None:
       await self.client.delete(key)

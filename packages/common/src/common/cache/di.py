from typing import Self

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from common.cache.repository import CacheRepository
from common.cache.settings import CacheSettings


class CacheProvider(Provider):
    @provide(scope=Scope.APP)
    def client(self: Self, settings: CacheSettings) -> Redis:
       return Redis.from_url(settings.dsn)

    @provide(scope=Scope.REQUEST)
    def repository(self: Self, client: Redis) -> CacheRepository:
        return CacheRepository(client=client)

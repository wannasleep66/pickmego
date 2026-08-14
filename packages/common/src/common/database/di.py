from collections.abc import AsyncGenerator
from typing import Self

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import make_async_session_factory
from common.database.settings import DatabaseSettings


class DatabaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def session(
        self: Self, settings: DatabaseSettings
    ) -> AsyncGenerator[AsyncSession]:
        async with (
            make_async_session_factory(dsn=settings.dsn)() as session,
            session.begin(),
        ):
            yield session

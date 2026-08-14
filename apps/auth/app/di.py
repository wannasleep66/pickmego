from typing import Self

from common.cache.di import CacheProvider
from common.cache.settings import CacheSettings
from common.database.di import DatabaseProvider
from common.database.settings import DatabaseSettings
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

from app.settings import AppSettings, Settings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def settings(self: Self) -> Settings:
        return Settings()

    @provide(scope=Scope.APP)
    def app(self: Self, settings: Settings) -> AppSettings:
        return settings.app

    @provide(scope=Scope.APP)
    def database(self: Self, settings: Settings) -> DatabaseSettings:
        return settings.database

    @provide(scope=Scope.APP)
    def cache(self: Self, settings: Settings) -> CacheSettings:
        return settings.cache


def make_container(*providers: Provider) -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        DatabaseProvider(),
        CacheProvider(),
        *providers,
    )

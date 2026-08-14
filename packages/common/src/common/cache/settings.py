from typing import Self

from pydantic_settings import BaseSettings


class CacheSettings(BaseSettings):
    host: str
    port: int
    db: int

    @property
    def dsn(self: Self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"

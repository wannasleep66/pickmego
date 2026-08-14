from typing import Self

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: int
    db: str

    @property
    def dsn(self: Self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    metadata = metadata


def make_async_engine(dsn: str, echo: bool = False) -> AsyncEngine:
    return create_async_engine(dsn, echo=echo)


def make_async_session_factory(dsn: str, echo: bool = False):
    return async_sessionmaker(
        bind=make_async_engine(dsn, echo=echo),
        expire_on_commit=False,
        autoflush=False,
        class_=AsyncSession,
    )

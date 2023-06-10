from contextlib import asynccontextmanager
from typing import Any
from databases import Database
from sqlalchemy import (
    create_engine,
    MetaData
)
import os
from sqlalchemy.ext.asyncio import (
    # async_sessionmaker,
    AsyncSession,
    create_async_engine,
    # AsyncAttrs,
)
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
)

from core.env import env
from .exceptions import (
    InitError,
    CloseError,
    DatabaseError
)
from core.log import LOG
from core.utils import singleton

db_url: str = "{}://{}:{}@{}:{}/{}".format(
        env("DB_SCHEME"),
        env("DB_USER"),
        env("DB_PASSWORD"),
        env("DB_HOST"),
        env("DB_PORT"),
        env("DB_NAME"),
)

if env("DEBUG") in ["1", 1, True, "true", "on", "yes"]:
    # db_url = "sqlite:///db.sqlite3"
    db_url = "sqlite://:memory:"


@singleton
class DatabaseClass(Database):
    """Singleton for Database class."""
    pass


@singleton
class MetaDataClass(MetaData):
    """Singleton for MetaData class."""
    pass


async def get_async_session() -> AsyncSession:
    """
    Creates an async session.
    """
    global db_url
    if "postgresql:" in db_url:
        db_url = db_url.replace("postgresql:", "postgresql+asyncpg:")
    engine = create_async_engine(db_url)

    #return async_sessionmaker(engine, expire_on_commit=False, class_=async_session)()
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)()


@asynccontextmanager
async def get_session():
    try:
        async_session = await get_async_session()

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()


class Base(DeclarativeBase):
    pass


# Base = declarative_base()

# @singleton
class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None
        self.init()

    def __getattr__(self, name) -> Any:
        return getattr(self._session, name)

    def init(self):
        global db_url
        if "postgresql:" in db_url:
            db_url = db_url.replace("postgresql:", "postgresql+asyncpg:")

        self._engine = create_async_engine(
            db_url,
            future=True,
            echo=False,
        )

        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    
    async def close_all(self) -> None:
        await self._session.close()
        await self._engine.dispose()


async def get_async_db() -> AsyncDatabaseSession:
    return AsyncDatabaseSession()

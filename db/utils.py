from contextlib import asynccontextmanager
from typing import Any
from tortoise import Tortoise

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


def get_db_url() -> str:
    """Return database URL."""
    global db_url
    # if "postgres:" in db_url:
    #     db_url = db_url.replace("postgres:", "postgres+asyncpg:")
    return db_url


def get_db_config() -> dict:
    """Return database configuration."""
    return {
        'connections': {
            'default': get_db_url()
        },
        'apps': {
            'models': {
                'models': ["db.models", "aerich.models"],
                'default_connection': 'default',
            }
        }
    }


async def create_database() -> None:
    """Initialize database connection."""
    try:
        await Tortoise.init(
            db_url=get_db_url(),
            modules={"models": ["db.models"]},
        )
        await Tortoise.generate_schemas()
    except Exception as e:
        LOG.error(e)
        raise InitError(e)


async def close_database() -> None:
    """Close database connection."""
    try:
        await Tortoise.close_connections()
    except Exception as e:
        LOG.error(e)
        raise CloseError(e)



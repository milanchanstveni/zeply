"""
Logging module.
"""
from pydantic import BaseModel
from logging.config import dictConfig
import logging


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "zeply"
    # LOG_FORMAT: str = "%(asctime)s | %(pathname)s: %(lineno)s | %(levelname)s | %(message)s"
    LOG_FORMAT: str = "%(levelname)s | %(pathname)s: %(lineno)s | %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt":  LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


dictConfig(LogConfig().dict())
#dictConfig(LogConfigDict)
# logging.getLogger('asyncio').setLevel(logging.WARNING)
LOG = logging.getLogger("zeply")

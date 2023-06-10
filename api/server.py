from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import uvicorn

from db.utils import (
    get_db_config,
    create_database,
    close_database
)
from core.log import LOG
from api.v0 import API0


@asynccontextmanager
async def startup_shutdown(app: FastAPI) -> None:
    LOG.info("Server started.")
    await create_database()
    yield
    await close_database()
    LOG.info("Server stopped.")


APP = FastAPI(
    title="Zeply",
    description='Zeply.',
    version="1.0",
    docs_url="/",
    lifespan=startup_shutdown
)

APP.include_router(API0)


register_tortoise(
    APP,
    config=get_db_config(),
    generate_schemas=True,
    add_exception_handlers=True,
)


if __name__ == "__main__":
    uvicorn.run(
        app="master.server:APP",
        host="0.0.0.0",
        port=5000,
        reload=True
    )

import asyncio
from collections.abc import AsyncGenerator

from common.http.error import use_exception_handlers
from common.http.middleware import use_middlewares
from common.logging import setup_logging
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from fastapi.routing import asynccontextmanager
from loguru import logger
from uvicorn import Config, Server

from app.di import make_container
from app.routes import use_routes
from app.settings import AppSettings


async def server() -> None:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
        yield

    container = make_container(FastapiProvider())

    settings = await container.get(AppSettings)

    app = FastAPI(lifespan=lifespan, title=settings.name)

    use_middlewares(app, allowed_origins=["*"])
    use_exception_handlers(app)
    use_routes(app)

    setup_dishka(container, app)

    await Server(config=Config(app=app, host=settings.host, port=settings.port)).serve()


async def bootstrap() -> None:
    settings = AppSettings()

    setup_logging(env=settings.env)

    apps = [server()]

    logger.info(
        "Bootstraping {app_name} application Env={env}",
        app_name=settings.name,
        env=settings.env,
    )

    try:
        await asyncio.gather(*apps)
    finally:
        logger.info("Shutdown")

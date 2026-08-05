import asyncio

from loguru import logger

from app.settings import Settings


async def bootstrap() -> None:
    logger.info("Started application")

    settings = Settings()

    logger.info("Loaded settings {settings}", settings=settings.model_dump())

    try:
        while True:
            await asyncio.sleep(10)
            logger.debug("Working")
    finally:
        logger.info("Shutdown application")

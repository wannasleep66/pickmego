from fastapi import FastAPI

from app.modules.health.router import router as health_router


def use_routes(app: FastAPI) -> None:
    app.include_router(health_router)

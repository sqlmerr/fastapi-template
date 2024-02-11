import dotenv
import os

from fastapi import FastAPI

from src.dependencies import init_dependencies
from src.api import root_router
from src.core import settings


def init_routers(app: FastAPI):
    app.include_router(root_router)


def create_app():
    app = FastAPI(
        title=settings.app_title,
        version=settings.version
    )
    init_routers(app)
    init_dependencies(app)
    return app

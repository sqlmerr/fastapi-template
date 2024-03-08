from contextlib import asynccontextmanager
from typing import TypeVar, Callable

from fastapi import FastAPI
from app.presentation.api import root_router
from app.ioc import IoC, InteractorFactory
from app.config import settings
from app.di import IocProvider

from dishka import make_async_container
from dishka.integrations.fastapi import (
    FromDishka,
    inject,
    setup_dishka,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Put here your logic
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_title,
        version=settings.version,
        lifespan=lifespan,
    )
    app.include_router(root_router)
    ioc = IoC()
    
    container = make_async_container(IocProvider(ioc))
    setup_dishka(container, app)

    return app

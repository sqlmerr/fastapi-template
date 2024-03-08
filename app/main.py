from contextlib import asynccontextmanager
from typing import TypeVar, Callable

from fastapi import FastAPI
from app.presentation.api import root_router
from app.ioc import IoC, InteractorFactory
from app.config import settings


DependencyT = TypeVar("DependencyT")


def singleton(value: DependencyT) -> Callable[[], DependencyT]:
    """Produce save value as a fastapi dependency."""

    def singleton_factory() -> DependencyT:
        return value

    return singleton_factory


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Put here your logic
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_title,
        version=settings.version,
        lifespan=lifespan,
    )
    app.include_router(root_router)
    ioc = IoC()
    app.dependency_overrides.update({InteractorFactory: singleton(ioc)})

    return app

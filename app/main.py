from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.api import root_router
from app.ioc import IoC
from app.config import settings
from app.di import init_di


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

    init_di(app, ioc)

    if settings.backend_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.backend_cors_origins,
            allow_methods=("GET", "POST"),
            allow_headers=("*"),
            allow_credentials=True,
        )

    return app

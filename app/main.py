from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.adapters.database.uow import UnitOfWork
from app.adapters.database.role import RoleGateway
from app.application.create_role import CreateRole
from app.application.register import Register
from app.config import settings
from app.di import init_di
from app.initial_data import create_initial_data
from app.presentation.api import root_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Put here your logic
    uow: UnitOfWork = await app.state.dishka_container.get(UnitOfWork)
    async with uow:
        await create_initial_data(CreateRole(uow, RoleGateway()))
        await uow.commit()
    yield
    await app.state.dishka_container.close()


def create_app(session_maker: Optional[async_sessionmaker] = None) -> FastAPI:
    app = FastAPI(
        title=settings.app_title,
        version=settings.version,
        lifespan=lifespan,
    )
    app.add_api_route("/", lambda: {"message": "Hello World"})
    app.include_router(root_router)

    init_di(app, session_maker)

    if settings.backend_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.backend_cors_origins,
            allow_methods=("GET", "POST"),
            allow_headers=("*",),
            allow_credentials=True,
        )

    return app

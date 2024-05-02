import asyncio

from typing import Optional

from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.adapters.database.post import PostGateway
from app.adapters.database.role import RoleGateway
from app.adapters.database.uow import UnitOfWork
from app.adapters.database.user import UserGateway
from app.application.authenticate import Authenticate
from app.application.common.db import session_maker
from app.application.common.uow import UoW
from app.application.create_post import CreatePost
from app.application.create_role import CreateRole
from app.application.delete_post import DeletePost
from app.application.get_all_posts import GetAllPosts
from app.application.get_all_roles import GetAllRoles
from app.application.get_post import GetPost
from app.application.get_role import GetRole
from app.application.register import Register
from app.application.update_post import UpdatePost


class InteractorProvider(Provider):
    def __init__(
        self, another_session_maker: Optional[async_sessionmaker] = None
    ) -> None:
        self.uow = UnitOfWork(another_session_maker or session_maker)
        self.user_gateway = UserGateway()
        self.post_gateway = PostGateway()
        self.role_gateway = RoleGateway()
        super().__init__()

    @provide(scope=Scope.APP)
    async def get_uow(self) -> UnitOfWork:
        return self.uow

    @provide(scope=Scope.REQUEST)
    async def get_role(self) -> GetRole:
        async with self.uow:
            return GetRole(self.uow, self.role_gateway)

    @provide(scope=Scope.REQUEST)
    async def get_all_roles(self) -> GetAllRoles:
        async with self.uow:
            return GetAllRoles(self.uow, self.role_gateway)

    @provide(scope=Scope.REQUEST)
    async def create_role(self) -> CreateRole:
        async with self.uow:
            return CreateRole(self.uow, self.role_gateway)

    @provide(scope=Scope.REQUEST)
    async def delete_role(self) -> DeletePost:
        async with self.uow:
            return DeletePost(self.uow, self.role_gateway)

    @provide(scope=Scope.REQUEST)
    async def authenticate(self) -> Authenticate:
        async with self.uow:
            return Authenticate(self.uow, self.user_gateway)

    @provide(scope=Scope.REQUEST)
    async def register(self) -> Register:
        async with self.uow:
            return Register(self.uow, self.user_gateway, self.role_gateway)

    @provide(scope=Scope.REQUEST)
    async def get_post(self) -> GetPost:
        async with self.uow:
            return GetPost(self.uow, self.post_gateway)

    @provide(scope=Scope.REQUEST)
    async def get_all_posts(self) -> GetAllPosts:
        async with self.uow:
            return GetAllPosts(self.uow, self.post_gateway)

    @provide(scope=Scope.REQUEST)
    async def create_post(self) -> CreatePost:
        async with self.uow:
            return CreatePost(self.uow, self.post_gateway, self.user_gateway)

    @provide(scope=Scope.REQUEST)
    async def delete_post(self) -> DeletePost:
        async with self.uow:
            return DeletePost(self.uow, self.post_gateway)

    @provide(scope=Scope.REQUEST)
    async def update_post(self) -> UpdatePost:
        async with self.uow:
            return UpdatePost(self.uow, self.post_gateway)


def init_di(app: FastAPI, sessionmaker: Optional[async_sessionmaker] = None) -> None:
    container = make_async_container(InteractorProvider(sessionmaker))
    setup_dishka(container, app)

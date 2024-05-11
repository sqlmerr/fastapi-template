from typing import Optional

from dishka import Provider, Scope, from_context, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.application.common.db import session_maker
from app.application.common.id_provider import IdProvider
from app.application.post.create_post import CreatePost
from app.application.post.delete_post import DeletePost
from app.application.post.get_all_posts import GetAllPosts
from app.application.post.get_post import GetPost
from app.application.post.update_post import UpdatePost
from app.application.role.create_role import CreateRole
from app.application.role.get_all_roles import GetAllRoles
from app.application.role.get_role import GetRole
from app.application.user.authenticate import Authenticate
from app.application.user.register import Register
from app.domain.services.access import AccessService
from app.infrastructure.auth.jwt import JwtTokenIdProvider, JwtTokenProcessor
from app.infrastructure.auth.password import PasswordProcessor
from app.infrastructure.gateway.post import PostGateway
from app.infrastructure.gateway.role import RoleGateway
from app.infrastructure.gateway.uow import UnitOfWork
from app.infrastructure.gateway.user import UserGateway


class InteractorProvider(Provider):
    def __init__(self, another_session_maker: Optional[async_sessionmaker] = None) -> None:
        self.uow = UnitOfWork(another_session_maker if another_session_maker is not None else session_maker)
        self.user_gateway = UserGateway()
        self.post_gateway = PostGateway()
        self.role_gateway = RoleGateway()
        super().__init__()

    @provide(scope=Scope.APP)
    async def get_uow(self) -> UnitOfWork:
        return self.uow

    @provide(scope=Scope.REQUEST)
    async def get_role(self, id_provider: IdProvider) -> GetRole:
        async with self.uow:
            return GetRole(
                self.uow,
                self.role_gateway,
                self.user_gateway,
                id_provider,
                access_service=AccessService(),
            )

    @provide(scope=Scope.REQUEST)
    async def get_all_roles(self, id_provider: IdProvider) -> GetAllRoles:
        async with self.uow:
            return GetAllRoles(
                self.uow,
                self.role_gateway,
                self.user_gateway,
                id_provider,
                access_service=AccessService(),
            )

    @provide(scope=Scope.REQUEST)
    async def create_role(self, id_provider: IdProvider) -> CreateRole:
        async with self.uow:
            return CreateRole(
                self.uow,
                self.role_gateway,
                self.user_gateway,
                id_provider,
                access_service=AccessService(),
            )

    @provide(scope=Scope.REQUEST)
    async def delete_role(self, id_provider: IdProvider) -> DeletePost:
        async with self.uow:
            return DeletePost(
                self.uow,
                self.post_gateway,
                self.user_gateway,
                id_provider,
                access_service=AccessService(),
            )

    @provide(scope=Scope.REQUEST)
    async def authenticate(self, password_processor: PasswordProcessor) -> Authenticate:
        async with self.uow:
            return Authenticate(self.uow, self.user_gateway, password_processor)

    @provide(scope=Scope.REQUEST)
    async def register(self) -> Register:
        async with self.uow:
            return Register(self.uow, self.user_gateway, self.role_gateway)

    @provide(scope=Scope.REQUEST)
    async def get_post(self, id_provider: IdProvider) -> GetPost:
        async with self.uow:
            return GetPost(
                self.uow,
                self.post_gateway,
                self.user_gateway,
                id_provider,
                access_service=AccessService(),
            )

    @provide(scope=Scope.REQUEST)
    async def get_all_posts(self, id_provider: IdProvider) -> GetAllPosts:
        async with self.uow:
            return GetAllPosts(self.uow, self.post_gateway, self.user_gateway, id_provider)

    @provide(scope=Scope.REQUEST)
    async def create_post(self, id_provider: IdProvider) -> CreatePost:
        async with self.uow:
            return CreatePost(
                self.uow,
                self.post_gateway,
                self.user_gateway,
                id_provider,
                access_service=AccessService(),
            )

    @provide(scope=Scope.REQUEST)
    async def delete_post(self, id_provider: IdProvider) -> DeletePost:
        async with self.uow:
            return DeletePost(
                self.uow,
                self.post_gateway,
                self.user_gateway,
                id_provider,
                access_service=AccessService(),
            )

    @provide(scope=Scope.REQUEST)
    async def update_post(self, id_provider: IdProvider) -> UpdatePost:
        async with self.uow:
            return UpdatePost(
                self.uow,
                self.post_gateway,
                self.user_gateway,
                id_provider,
                access_service=AccessService(),
            )


class AuthAdaptersProvider(Provider):
    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_jwt_token_processor(self) -> JwtTokenProcessor:
        return JwtTokenProcessor()

    @provide(scope=Scope.APP)
    def get_password_processor(self) -> PasswordProcessor:
        return PasswordProcessor()

    @provide(scope=Scope.REQUEST)
    def get_id_provider(self, request: Request, token_processor: JwtTokenProcessor) -> IdProvider:
        _, token = request.headers.get("Authorization").split("Bearer ")
        id_provider = JwtTokenIdProvider(token_processor=token_processor, token=token)
        return id_provider


def init_di(app: FastAPI, sessionmaker: Optional[async_sessionmaker] = None) -> None:
    container = make_async_container(InteractorProvider(sessionmaker), AuthAdaptersProvider())
    setup_dishka(container, app)

from contextlib import asynccontextmanager

from app.adapters.database.uow import UnitOfWork
from app.adapters.database.user import UserGateway
from app.adapters.database.post import PostGateway
from app.application.authenticate import Authenticate
from app.application.create_post import CreatePost
from app.application.delete_post import DeletePost
from app.application.get_all_posts import GetAllPosts
from app.application.register import Register
from app.application.get_post import GetPost
from app.application.update_post import UpdatePost
from app.presentation.interactor_factory import InteractorFactory
from app.application.common.db import session_maker


class IoC(InteractorFactory):
    def __init__(self) -> None:
        self.uow = UnitOfWork(session_maker)
        self.user_gateway = UserGateway()
        self.post_gateway = PostGateway()

    @asynccontextmanager
    async def authenticate(self) -> Authenticate:
        yield Authenticate(self.uow, self.user_gateway)

    @asynccontextmanager
    async def register(self) -> Register:
        yield Register(self.uow, self.user_gateway)

    @asynccontextmanager
    async def get_post(self) -> GetPost:
        yield GetPost(self.uow, self.post_gateway)

    @asynccontextmanager
    async def get_all_posts(self) -> GetAllPosts:
        yield GetAllPosts(self.uow, self.post_gateway)

    @asynccontextmanager
    async def create_post(self) -> CreatePost:
        yield CreatePost(self.uow, self.post_gateway, self.user_gateway)

    @asynccontextmanager
    async def delete_post(self) -> DeletePost:
        yield DeletePost(self.uow, self.post_gateway)

    @asynccontextmanager
    async def update_post(self) -> UpdatePost:
        yield UpdatePost(self.uow, self.post_gateway)

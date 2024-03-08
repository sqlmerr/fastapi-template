from contextlib import asynccontextmanager

from app.adapters.database.uow import UnitOfWork
from app.adapters.database.user import UserGateway
from app.application.authenticate import Authenticate
from app.application.register import Register
from app.presentation.interactor_factory import InteractorFactory
from app.application.common.db import session_maker


class IoC(InteractorFactory):
    def __init__(self) -> None:
        self.uow = UnitOfWork(session_maker)
        self.user_gateway = UserGateway()

    @asynccontextmanager
    async def authenticate(self) -> Authenticate:
        yield Authenticate(self.uow, self.user_gateway)

    @asynccontextmanager
    async def register(self) -> Register:
        yield Register(self.uow, self.user_gateway)

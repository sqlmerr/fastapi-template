from abc import ABC, abstractmethod
from typing import Any, Type

from src.core.repositories.users import UsersRepository


class IUnitOfWork(ABC):
    users: Type[UsersRepository]
    
    @abstractmethod
    def __init__(self, session_factory: Any):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UOW(IUnitOfWork):
    def __init__(self, session_factory: Any):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.application.common.uow import UoW


class UnitOfWork(UoW):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self.session_factory = session_factory

    async def __aenter__(self, *args, **kwargs) -> AsyncSession:
        self.session = self.session_factory()
        return self.session

    async def __aexit__(self, *args, **kwargs):
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()

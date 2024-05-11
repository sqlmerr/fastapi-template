from sqlalchemy.ext.asyncio import async_sessionmaker

from app.application.common.uow import UoW


class UnitOfWork(UoW):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self.session_factory = session_factory
        self.session = None

    async def __aenter__(self, *args, **kwargs) -> UoW:
        if self.session is None:
            self.session = self.session_factory()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.session.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()

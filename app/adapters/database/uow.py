from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.application.common.uow import UoW


class UnitOfWork(UoW):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self.session = session_factory()
        self.session: AsyncSession

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()

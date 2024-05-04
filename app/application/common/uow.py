from abc import abstractmethod
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class UoW(Protocol):
    session: AsyncSession

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def flush(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

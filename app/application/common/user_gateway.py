from abc import abstractmethod
from typing import Protocol, Optional

from app.domain.entities.user import User
from app.application.common.uow import UoW
from app.application.schemas.user import UserUpdateSchema, UserCreateSchema


class UserReader(Protocol):
    @abstractmethod
    async def get_user(self, user_id: int, uow: UoW) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_filters(self, uow: UoW, **filter_by) -> Optional[User]:
        raise NotImplementedError


class UserSaver(Protocol):
    @abstractmethod
    async def save_user(
        self, user_id: int, user: UserUpdateSchema, uow: UoW
    ) -> Optional[User]:
        raise NotImplementedError


class UserCreator(Protocol):
    @abstractmethod
    async def create_user(self, user: UserCreateSchema, uow: UoW) -> Optional[User]:
        raise NotImplementedError

from abc import abstractmethod
from typing import Optional, Protocol
from uuid import UUID

from app.application.common.uow import UoW
from app.application.schemas.user import UserCreateSchema, UserUpdateSchema
from app.domain.entities.role import Role
from app.domain.entities.user import User


class UserReader(Protocol):
    @abstractmethod
    async def get_user(self, user_id: UUID, uow: UoW) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_filters(self, uow: UoW, **filter_by) -> Optional[User]:
        raise NotImplementedError


class UserSaver(Protocol):
    @abstractmethod
    async def save_user(self, user_id: UUID, user: UserUpdateSchema, uow: UoW) -> Optional[User]:
        raise NotImplementedError


class UserCreator(Protocol):
    @abstractmethod
    async def create_user(self, user: UserCreateSchema, role: Role, uow: UoW) -> Optional[User]:
        raise NotImplementedError

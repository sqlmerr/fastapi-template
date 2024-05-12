from abc import abstractmethod
from typing import Any, Protocol
from uuid import UUID

from app.application.common.uow import UoW
from app.domain.entities.role import Role


class RoleReader(Protocol):
    @abstractmethod
    async def get_role(self, role_id: UUID, uow: UoW) -> Role | None:
        raise NotImplementedError

    @abstractmethod
    async def get_role_filters(self, uow: UoW, **filter_by) -> Role | None:
        raise NotImplementedError

    @abstractmethod
    async def get_roles(self, uow: UoW) -> list[Role]:
        raise NotImplementedError


class RoleSaver(Protocol):
    @abstractmethod
    async def save_role(self, role_id: UUID, data: dict[str, Any], uow: UoW) -> bool:
        raise NotImplementedError


class RoleCreator(Protocol):
    @abstractmethod
    async def create_role(self, role: dict[str, Any], uow: UoW) -> UUID | None:
        raise NotImplementedError


class RoleDeleter(Protocol):
    @abstractmethod
    async def delete_role(self, role_id: UUID | str, uow: UoW) -> bool:
        raise NotImplementedError

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.id_provider import IdProvider
from app.application.common.interactor import Interactor
from app.application.common.role_gateway import RoleDeleter, RoleReader
from app.application.common.user_gateway import UserReader
from app.domain.services.access import AccessService


class RoleReaderAndDeleter(RoleReader, RoleDeleter, Protocol):
    pass


@dataclass(frozen=True)
class DeleteRole(Interactor[UUID | str, bool]):
    role_reader_and_deleter: RoleReaderAndDeleter
    user_reader: UserReader
    id_provider: IdProvider
    access_service: AccessService

    async def __call__(self, data: UUID | str) -> bool:
        user_id = self.id_provider.get_current_user_id()
        user = await self.user_reader.get_user(user_id, self.uow)
        self.access_service.ensure_has_permissions(user.role_permissions, ["roles:delete"])

        if isinstance(data, str):
            role = await self.role_reader_and_deleter.get_role_filters(self.uow, name=data)
        else:
            role = await self.role_reader_and_deleter.get_role(data, self.uow)
        if role is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
        result = await self.role_reader_and_deleter.delete_role(data, self.uow)
        await self.uow.commit()

        return result

from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.role_gateway import RoleDeleter, RoleReader
from app.application.common.uow import UoW


class RoleReaderAndDeleter(RoleReader, RoleDeleter):
    pass


class DeleteRole(Interactor[UUID, bool]):
    def __init__(self, uow: UoW, role_reader_and_deleter: RoleReaderAndDeleter):
        self.uow = uow
        self.role_reader_and_deleter = role_reader_and_deleter

    async def __call__(self, data: UUID) -> bool:
        role = await self.role_reader_and_deleter.get_role(data, self.uow)
        if role is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
        result = await self.role_reader_and_deleter.delete_role(data, self.uow)

        return result

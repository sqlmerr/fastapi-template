from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.role_gateway import RoleReader
from app.application.common.uow import UoW
from app.application.schemas.role import RoleSchema


class GetRole(Interactor[UUID, RoleSchema | None]):
    def __init__(self, uow: UoW, role_reader: RoleReader):
        self.uow = uow
        self.role_reader = role_reader

    async def __call__(self, data: UUID) -> RoleSchema | None:
        role = await self.role_reader.get_role(data, self.uow)
        if role is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")

        return RoleSchema.model_validate(role, from_attributes=True)

from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.role_gateway import RoleReader
from app.application.common.uow import UoW
from app.application.schemas.role import RoleSchema


class GetAllRoles(Interactor[UUID, list[RoleSchema]]):
    def __init__(self, uow: UoW, role_reader: RoleReader):
        self.uow = uow
        self.role_reader = role_reader

    async def __call__(self) -> list[RoleSchema]:
        roles = await self.role_reader.get_roles(self.uow)
        if not roles:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Roles not found")

        return [
            RoleSchema.model_validate(role[0], from_attributes=True) for role in roles
        ]

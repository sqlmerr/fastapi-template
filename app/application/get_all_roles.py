from dataclasses import dataclass

from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.role_gateway import RoleReader
from app.application.schemas.role import RoleSchema


@dataclass(frozen=True)
class GetAllRolesDTO:
    limit: int = 10
    offset: int = 0


@dataclass(frozen=True)
class GetAllRoles(Interactor[GetAllRolesDTO, list[RoleSchema]]):
    role_reader: RoleReader

    async def __call__(self, data: GetAllRolesDTO) -> list[RoleSchema]:
        roles = await self.role_reader.get_roles(self.uow)
        if not roles:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Roles not found")

        return [
            RoleSchema.model_validate(role[0], from_attributes=True) for role in roles
        ]

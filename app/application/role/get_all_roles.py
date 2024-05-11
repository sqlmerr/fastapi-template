from dataclasses import dataclass, field

from fastapi import HTTPException, status

from app.application.common.id_provider import IdProvider
from app.application.common.interactor import Interactor
from app.application.common.role_gateway import RoleReader
from app.application.common.user_gateway import UserReader
from app.application.schemas.role import RoleSchema
from app.domain.services.access import AccessService


@dataclass(frozen=True)
class GetAllRolesDTO:
    limit: int = 10
    offset: int = 0


@dataclass(frozen=True)
class GetAllRoles(Interactor[GetAllRolesDTO, list[RoleSchema]]):
    role_reader: RoleReader
    user_reader: UserReader
    id_provider: IdProvider
    access_service: AccessService = field(default_factory=AccessService)

    async def __call__(self, data: GetAllRolesDTO) -> list[RoleSchema]:
        user_id = self.id_provider.get_current_user_id()
        user = await self.user_reader.get_user(user_id, self.uow)
        self.access_service.ensure_has_permissions(user.role_permissions, ["roles:read"])

        roles = await self.role_reader.get_roles(self.uow)
        if not roles:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Roles not found")

        return [RoleSchema.model_validate(role[0], from_attributes=True) for role in roles]

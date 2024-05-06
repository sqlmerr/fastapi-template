from dataclasses import dataclass
from uuid import UUID

from app.application.common.interactor import Interactor
from app.application.common.role_gateway import RoleCreator
from app.application.schemas.role import RoleCreateSchema


@dataclass(frozen=True)
class CreateRole(Interactor[RoleCreateSchema, UUID | None]):
    role_creator: RoleCreator

    async def __call__(self, data: RoleCreateSchema) -> UUID | None:
        role_id = await self.role_reader.create_role(data, self.uow)
        await self.uow.commit()
        return role_id

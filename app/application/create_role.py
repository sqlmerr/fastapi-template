from uuid import UUID

from app.application.common.interactor import Interactor
from app.application.common.role_gateway import RoleCreator
from app.application.common.uow import UoW
from app.application.schemas.role import RoleCreateSchema


class CreateRole(Interactor[RoleCreateSchema, UUID | None]):
    def __init__(self, uow: UoW, role_creator: RoleCreator):
        self.uow = uow
        self.role_reader = role_creator

    async def __call__(self, data: RoleCreateSchema) -> UUID | None:
        role_id = await self.role_reader.create_role(data, self.uow)
        return role_id

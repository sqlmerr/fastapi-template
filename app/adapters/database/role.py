from uuid import UUID

from sqlalchemy import delete, insert, select, update

from app.application.common.role_gateway import (
    RoleCreator,
    RoleDeleter,
    RoleReader,
    RoleSaver,
)
from app.application.common.uow import UoW
from app.application.schemas.role import RoleCreateSchema, RoleUpdateSchema
from app.domain.entities.role import Role


class RoleGateway(RoleReader, RoleCreator, RoleDeleter, RoleSaver):
    async def get_role(self, role_id: UUID, uow: UoW) -> Role | None:
        return await self.get_role_filters(uow, id=role_id)

    async def get_role_filters(self, uow: UoW, **filter_by) -> Role | None:
        stmt = select(Role).filter_by(**filter_by)
        result = await uow.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_roles(self, uow: UoW) -> list[Role]:
        stmt = select(Role)
        result = await uow.session.execute(stmt)
        return result.all()

    async def create_role(self, role: RoleCreateSchema, uow: UoW) -> UUID | None:
        stmt = insert(Role).values(**role.model_dump()).returning(Role.id)
        result = await uow.session.execute(stmt)
        return result.scalar_one_or_none()

    async def save_role(self, role_id: UUID, data: RoleUpdateSchema, uow: UoW) -> bool:
        stmt = update(Role).values(**data.model_dump()).where(Role.id == role_id)
        await uow.session.execute(stmt)
        return True

    async def delete_role(self, role_id: UUID, uow: UoW) -> bool:
        stmt = delete(Role).where(Role.id == role_id)
        await uow.session.execute(stmt)
        return True

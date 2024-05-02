from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import insert, select, update

from app.application.common.uow import UoW
from app.application.common.user_gateway import UserCreator, UserReader, UserSaver
from app.application.schemas.user import UserCreateSchema, UserUpdateSchema
from app.domain.entities.role import Role
from app.domain.entities.user import User


class UserGateway(UserReader, UserSaver, UserCreator):
    async def get_user(self, user_id: UUID, uow: UoW) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await uow.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_filters(self, uow: UoW, **filter_by) -> Optional[User]:
        stmt = select(User).filter_by(**filter_by)
        user = await uow.session.execute(stmt)
        return user.scalar_one_or_none()

    async def save_user(
        self, user_id: UUID, user: UserUpdateSchema, uow: UoW
    ) -> Optional[User]:
        user_dict = user.model_dump()
        if not user_dict:
            return

        stmt = update(User).values(**user_dict).where(User.id == user_id)
        result = await uow.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(
        self, user: UserCreateSchema, role: Role, uow: UoW
    ) -> UUID | None:
        user_dict = user.model_dump()
        if not user_dict:
            return

        stmt = (
            insert(User)
            .values(**user_dict, registered_at=datetime.utcnow(), role_id=role.id)
            .returning(User.id)
        )
        result = await uow.session.execute(stmt)
        return result.scalar_one_or_none()

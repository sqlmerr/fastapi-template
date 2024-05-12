from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.orm import joinedload

from app.application.common.uow import UoW
from app.application.common.user_gateway import UserCreator, UserReader, UserSaver
from app.domain.entities.role import Role
from app.domain.entities.user import User


class UserGateway(UserReader, UserSaver, UserCreator):
    async def get_user(self, user_id: UUID, uow: UoW) -> User:
        return await self.get_user_filters(uow, id=user_id)

    async def get_user_filters(self, uow: UoW, **filter_by) -> Optional[User]:
        stmt = select(User).options(joinedload(User.role)).filter_by(**filter_by)
        user = await uow.session.execute(stmt)
        return user.scalar_one_or_none()

    async def save_user(self, user_id: UUID, user: dict[str, Any], uow: UoW) -> Optional[User]:
        if not user:
            return

        stmt = update(User).values(**user).where(User.id == user_id)
        result = await uow.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user: dict[str, Any], role: Role, uow: UoW) -> UUID | None:
        if not user:
            return

        stmt = insert(User).values(**user, registered_at=datetime.utcnow(), role_id=role.id).returning(User.id)
        result = await uow.session.execute(stmt)
        return result.scalar_one_or_none()

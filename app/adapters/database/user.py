from sqlalchemy import select, update, insert
from typing import Optional

from app.application.common.user_gateway import UserSaver, UserReader, UserCreator

from app.application.common.uow import UoW
from app.domain.entities.user import User
from app.application.schemas.user import UserUpdateSchema, UserCreateSchema


class UserGateway(UserReader, UserSaver, UserCreator):
    async def get_user(self, user_id: int, uow: UoW) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await uow.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_filters(self, uow: UoW, **filter_by) -> Optional[User]:
        stmt = select(User).filter_by(**filter_by)
        user = await uow.session.execute(stmt)
        return user.scalar_one_or_none()

    async def save_user(
        self, user_id: int, user: UserUpdateSchema, uow: UoW
    ) -> Optional[User]:
        user_dict = user.model_dump()
        if not user_dict:
            return

        stmt = update(User).values(**user_dict).where(User.id == user_id)
        result = await uow.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user: UserCreateSchema, uow: UoW) -> Optional[bool]:
        user_dict = user.model_dump()
        if not user_dict:
            return

        stmt = insert(User).values(**user_dict)
        await uow.session.execute(stmt)
        return True
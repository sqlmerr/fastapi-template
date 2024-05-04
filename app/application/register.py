from typing import Union
from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.role_gateway import RoleReader
from app.application.common.uow import UoW
from app.application.common.user_gateway import UserCreator, UserReader
from app.application.schemas.user import UserCreateSchema


class Register(Interactor[UserCreateSchema, bool | UUID]):
    def __init__(
        self,
        uow: UoW,
        user_creator_and_reader: Union[UserCreator, UserReader],
        role_reader: RoleReader,
    ) -> None:
        self.uow = uow
        self.user_creator_and_reader = user_creator_and_reader
        self.role_reader = role_reader

    async def __call__(
        self, data: UserCreateSchema, role_name: str = "user"
    ) -> bool | UUID:
        if (
            await self.user_creator_and_reader.get_user_filters(
                self.uow, username=data.username
            )
            is not None
        ):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Username is already taken")

        role = await self.role_reader.get_role_filters(self.uow, name=role_name)
        result = await self.user_creator_and_reader.create_user(data, role, self.uow)
        await self.uow.commit()
        if isinstance(result, UUID):
            return result
        return True

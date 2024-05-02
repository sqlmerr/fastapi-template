from uuid import UUID
from typing import Union
from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.uow import UoW
from app.application.schemas.user import UserCreateSchema
from app.application.common.user_gateway import UserCreator, UserReader


class Register(Interactor[UserCreateSchema, bool | UUID]):
    def __init__(
        self, uow: UoW, user_creator_and_reader: Union[UserCreator, UserReader]
    ) -> None:
        self.uow = uow
        self.user_creator_and_reader = user_creator_and_reader

    async def __call__(self, data: UserCreateSchema) -> bool | UUID:
        if (
            await self.user_creator_and_reader.get_user_filters(
                self.uow, username=data.username
            )
            is not None
        ):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Username is already taken")

        result = await self.user_creator_and_reader.create_user(data, self.uow)
        await self.uow.commit()
        if isinstance(result, UUID):
            return result
        return True

from dataclasses import dataclass
from typing import Union
from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.role_gateway import RoleReader
from app.application.common.uow import UoW
from app.application.common.user_gateway import UserCreator, UserReader
from app.application.schemas.user import UserCreateSchema


@dataclass(frozen=True)
class RegisterDTO:
    data: UserCreateSchema
    role_name: str = "user"


class Register(Interactor[RegisterDTO, bool | UUID]):
    def __init__(
        self,
        uow: UoW,
        user_creator_and_reader: Union[UserCreator, UserReader],
        role_reader: RoleReader,
    ) -> None:
        self.uow = uow
        self.user_creator_and_reader = user_creator_and_reader
        self.role_reader = role_reader

    async def __call__(self, data: RegisterDTO) -> bool | UUID:
        if (
            await self.user_creator_and_reader.get_user_filters(
                self.uow, username=data.data.username
            )
            is not None
        ):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Username is already taken")

        role = await self.role_reader.get_role_filters(self.uow, name=data.role_name)
        if role is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, f"Role {data.role_name} not found"
            )

        result = await self.user_creator_and_reader.create_user(
            data.data, role, self.uow
        )
        await self.uow.commit()
        if isinstance(result, UUID):
            return result
        return True

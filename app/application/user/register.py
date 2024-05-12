from dataclasses import asdict, dataclass
from typing import Protocol
from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.role_gateway import RoleReader
from app.application.common.user_gateway import UserCreator, UserReader


@dataclass(frozen=True)
class RegisterDTO:
    username: str
    password: str
    role_name: str = "user"


class UserCreatorAndReader(UserCreator, UserReader, Protocol):
    pass


@dataclass(frozen=True)
class Register(Interactor[RegisterDTO, bool | UUID]):
    user_creator_and_reader: UserCreatorAndReader
    role_reader: RoleReader

    async def __call__(self, data: RegisterDTO) -> bool | UUID:
        if await self.user_creator_and_reader.get_user_filters(self.uow, username=data.username) is not None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Username is already taken")

        role = await self.role_reader.get_role_filters(self.uow, name=data.role_name)
        if role is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Role {data.role_name} not found")

        result = await self.user_creator_and_reader.create_user(asdict(data), role, self.uow)
        await self.uow.commit()
        if isinstance(result, UUID):
            return result
        return True

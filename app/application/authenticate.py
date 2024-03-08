from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.uow import UoW
from app.application.common.user_gateway import UserReader
from app.application.schemas.user import UserSchema


class LoginDTO(BaseModel):
    username: str


class Authenticate(Interactor[LoginDTO, int]):
    def __init__(self, uow: UoW, user_reader: UserReader) -> None:
        self.uow = uow
        self.user_reader = user_reader

    async def __call__(self, data: LoginDTO) -> Optional[int]:
        data_dict = data.model_dump()
        result = await self.user_reader.get_user_filters(self.uow, **data_dict)
        if result is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return UserSchema(
            id=result.id,
            username=result.username
        )

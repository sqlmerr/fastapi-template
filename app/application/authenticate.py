from dataclasses import dataclass
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel

from app.application.common.interactor import Interactor
from app.application.common.user_gateway import UserReader
from app.application.schemas.user import UserSchema
from app.utils.jwt import verify_password


class LoginDTO(BaseModel):
    username: str
    password: Optional[str] = None


@dataclass(frozen=True)
class Authenticate(Interactor[LoginDTO, UserSchema]):
    user_reader: UserReader

    async def __call__(
        self, data: LoginDTO, password_verify: bool = True
    ) -> Optional[UserSchema]:
        result = await self.user_reader.get_user_filters(
            self.uow, username=data.username
        )
        if result is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        user = UserSchema.model_validate(result, from_attributes=True)
        if (
            password_verify
            and data.password is not None
            and not verify_password(data.password, result.password)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

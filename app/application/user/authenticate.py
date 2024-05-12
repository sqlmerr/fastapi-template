from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.application.common.interactor import Interactor
from app.application.common.user_gateway import UserReader
from app.application.schemas import UserSchema
from app.domain.exceptions.access import AuthenticationError
from app.infrastructure.auth.password import PasswordProcessor


@dataclass(frozen=True)
class LoginDTO(BaseModel):
    id: UUID | None = None
    username: str | None = None
    password: str | None = None


@dataclass(frozen=True)
class Authenticate(Interactor[LoginDTO, UserSchema]):
    user_reader: UserReader
    password_processor: PasswordProcessor

    async def __call__(self, data: LoginDTO, password_verify: bool = True) -> Optional[UserSchema]:
        if not data.id and not data.username:
            raise AuthenticationError

        if data.id:
            result = await self.user_reader.get_user(data.id, self.uow)
        else:
            result = await self.user_reader.get_user_filters(self.uow, username=data.username)

        if result is None:
            raise AuthenticationError
        user = UserSchema.model_validate(result, from_attributes=True)
        if (
            password_verify
            and data.password is not None
            and not self.password_processor.verify_password(data.password, result.password)
        ):
            raise AuthenticationError
        return user

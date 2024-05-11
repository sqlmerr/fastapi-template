from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from app.application.common.id_provider import IdProvider
from app.config import settings
from app.domain.exceptions.access import AuthenticationError


@dataclass(frozen=True)
class JwtTokenProcessor:
    algorithm: str = "HS256"
    expire: timedelta = timedelta(minutes=30)

    def validate_access_token(self, token: str):
        try:
            data = jwt.decode(
                token,
                settings.secret_key.get_secret_value(),
                algorithms=[self.algorithm],
            )
        except jwt.PyJWTError:
            raise AuthenticationError

        if not data.get("sub"):
            raise AuthenticationError

        return UUID(data.get("sub"))

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + self.expire
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=self.algorithm)
        return encoded_jwt


@dataclass(frozen=True)
class JwtTokenIdProvider(IdProvider):
    token_processor: JwtTokenProcessor
    token: str

    def get_current_user_id(self) -> UUID:
        return self.token_processor.validate_access_token(self.token)

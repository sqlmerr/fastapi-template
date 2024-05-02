from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: UUID
    username: str
    registered_at: datetime
    disabled: bool


class UserUpdateSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(BaseModel):
    username: str
    password: str

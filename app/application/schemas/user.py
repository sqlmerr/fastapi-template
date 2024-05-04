from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: UUID
    username: str
    registered_at: datetime
    disabled: bool
    role_id: UUID


class UserUpdateSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(BaseModel):
    username: str
    password: str

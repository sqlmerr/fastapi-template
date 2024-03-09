from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    registered_at: datetime


class UserUpdateSchema(BaseModel):
    username: str


class UserCreateSchema(BaseModel):
    username: str

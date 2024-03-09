from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    registered_at: datetime
    disabled: bool


class UserUpdateSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(BaseModel):
    username: str
    password: str

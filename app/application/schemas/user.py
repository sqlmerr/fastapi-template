from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str


class UserUpdateSchema(BaseModel):
    username: str


class UserCreateSchema(BaseModel):
    username: str

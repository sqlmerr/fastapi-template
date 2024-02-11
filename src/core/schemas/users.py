from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    

class UserSchemaAdd(BaseModel):
    username: str


class UserSchemaEdit(BaseModel):
    username: str


class UserGetResponse(BaseModel):
    user: UserSchema


class UserCreateResponse(BaseModel):
    user_id: int


class UserEditResponse(BaseModel):
    user_id: int


class UserDeleteResponse(BaseModel):
    status: bool

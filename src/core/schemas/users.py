from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    

class UserSchemaAdd(BaseModel):
    username: str

from pydantic import BaseModel


class PostSchema(BaseModel):
    id: int
    text: str
    author_id: int


class PostSchemaCreate(BaseModel):
    text: str


class PostSchemaUpdate(BaseModel):
    text: str

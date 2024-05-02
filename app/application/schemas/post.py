from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PostSchema(BaseModel):
    id: UUID
    text: str
    author_id: UUID


class PostSchemaCreate(BaseModel):
    text: str


class PostSchemaUpdate(BaseModel):
    text: Optional[str] = None

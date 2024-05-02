from uuid import UUID

from pydantic import BaseModel


class RoleSchema(BaseModel):
    id: UUID
    name: str
    description: str
    permissions: list[str]


class RoleCreateSchema(BaseModel):
    name: str
    description: str
    permissions: list[str]


class RoleUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    permissions: list[str] | None = None

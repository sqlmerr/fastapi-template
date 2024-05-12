from typing import Any
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from app.application.common.dto import Pagination
from app.application.role.create_role import CreateRole, CreateRoleDTO
from app.application.role.delete_role import DeleteRole
from app.application.role.get_all_roles import GetAllRoles
from app.application.role.get_role import GetRole
from app.application.schemas import RoleCreateSchema, RoleSchema
from app.presentation.api.dependencies import OAuth2Depends

router = APIRouter(prefix="/roles", tags=["roles"], route_class=DishkaRoute)


@router.get(
    "/{role_id}",
    dependencies=[OAuth2Depends],
)
async def get_role_by_id(role_id: UUID, interactor: FromDishka[GetRole]) -> RoleSchema:
    return await interactor(role_id)


@router.get("/", dependencies=[OAuth2Depends])
async def get_roles(interactor: FromDishka[GetAllRoles]) -> list[RoleSchema]:
    return await interactor(Pagination())


@router.post(
    "/",
    dependencies=[OAuth2Depends],
)
async def create_role(data: RoleCreateSchema, interactor: FromDishka[CreateRole]) -> dict[str, Any]:
    return {"role_id": await interactor(CreateRoleDTO(**data.model_dump()))}


@router.delete("/", dependencies=[OAuth2Depends])
async def delete_role(role_id: UUID, interactor: FromDishka[DeleteRole]):
    return {"status": await interactor(role_id)}

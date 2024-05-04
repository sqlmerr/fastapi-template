from typing import Any
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from app.application.create_role import CreateRole
from app.application.delete_role import DeleteRole
from app.application.get_all_roles import GetAllRoles
from app.application.get_role import GetRole
from app.application.schemas.role import RoleCreateSchema, RoleSchema

from ..dependencies import get_current_user_with_permissions

router = APIRouter(prefix="/roles", tags=["roles"], route_class=DishkaRoute)


@router.get(
    "/{role_id}",
    dependencies=[Depends(get_current_user_with_permissions(["roles:read"]))],
)
async def get_role_by_id(role_id: UUID, interactor: FromDishka[GetRole]) -> RoleSchema:
    return await interactor(role_id)


@router.get(
    "/", dependencies=[Depends(get_current_user_with_permissions(["roles:read"]))]
)
async def get_roles(interactor: FromDishka[GetAllRoles]) -> list[RoleSchema]:
    return await interactor()


@router.post(
    "/",
    dependencies=[
        Depends(get_current_user_with_permissions(["roles:create"])),
    ],
)
async def create_role(
    data: RoleCreateSchema, interactor: FromDishka[CreateRole]
) -> dict[str, Any]:
    return {"role_id": await interactor(data)}


@router.delete(
    "/", dependencies=[Depends(get_current_user_with_permissions(["roles:delete"]))]
)
async def delete_role(role_id: UUID, interactor: FromDishka[DeleteRole]):
    return {"status": await interactor(role_id)}

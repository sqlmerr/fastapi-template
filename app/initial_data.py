from contextlib import suppress
from typing import Protocol
from fastapi import HTTPException

from app.application.common.role_gateway import RoleSaver, RoleDeleter, RoleCreator, RoleReader
from app.application.common.uow import UoW
from app.application.create_role import CreateRole
from app.application.delete_role import DeleteRole
from app.application.get_role import GetRole
from app.application.register import Register
from app.application.schemas.role import RoleCreateSchema
from app.application.schemas.user import UserCreateSchema
from app.config import settings
from app.utils.jwt import get_password_hash


class RoleGateway(RoleReader, RoleCreator, RoleDeleter, RoleSaver, Protocol):
    pass


async def create_initial_data(uow: UoW, role_gateway: RoleGateway, create_user: Register) -> None:
    user_role = await role_gateway.get_role_filters(uow, name="user")
    admin_role = await role_gateway.get_role_filters(uow, name="admin")

    if not user_role:
        await role_gateway.create_role(
            RoleCreateSchema(
                name="user",
                description="User role",
                permissions=[
                    "posts:read",
                    "posts:update",
                    "posts:create",
                    "posts:delete",
                ],
            ),
            uow
        )

    if not admin_role:
        await role_gateway.create_role(
            RoleCreateSchema(
                name="admin",
                description="Admin Role",
                permissions=["*"],
            ),
            uow
        )

    with suppress(HTTPException):
        await create_user(
            UserCreateSchema(
                username="admin",
                password=get_password_hash(settings.admin_password.get_secret_value()),
            ),
            "admin",
        )

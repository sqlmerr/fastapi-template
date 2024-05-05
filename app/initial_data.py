from contextlib import suppress

from fastapi import HTTPException

from app.adapters.database.role import RoleGateway
from app.adapters.database.uow import UnitOfWork
from app.adapters.database.user import UserGateway
from app.application.common.db import session_maker
from app.application.common.uow import UoW
from app.application.register import Register, RegisterDTO
from app.application.schemas.role import RoleCreateSchema
from app.application.schemas.user import UserCreateSchema
from app.config import settings
from app.utils.jwt import get_password_hash


async def create_initial_data(
    uow: UoW, role_gateway: RoleGateway, create_user: Register
) -> None:
    user_role = await role_gateway.get_role_filters(uow, name="user")
    admin_role = await role_gateway.get_role_filters(uow, name="admin")

    if not user_role:
        print("Creating user role")
        await role_gateway.create_role(
            RoleCreateSchema(
                name="user",
                description="User role",
                permissions=[
                    "posts:read",
                    "posts:update",
                    "posts:create",
                    "posts:delete",
                    "roles:read",
                ],
            ),
            uow,
        )

    if not admin_role:
        print("Creating admin role")
        await role_gateway.create_role(
            RoleCreateSchema(
                name="admin",
                description="Admin Role",
                permissions=["*"],
            ),
            uow,
        )

    with suppress(HTTPException):
        await create_user(
            RegisterDTO(
                UserCreateSchema(
                    username="admin",
                    password=get_password_hash(
                        settings.admin_password.get_secret_value()
                    ),
                ),
                "admin",
            )
        )
        print("Created admin")
    print("Successfully!")


async def main():
    print("Initializing db...")
    role_gateway = RoleGateway()
    uow = UnitOfWork(session_maker)
    async with uow:
        await create_initial_data(
            uow, role_gateway, Register(uow, UserGateway(), role_gateway)
        )

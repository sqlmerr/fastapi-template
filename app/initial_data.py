from contextlib import suppress

from fastapi import HTTPException

from app.application.common.db import session_maker
from app.application.common.uow import UoW
from app.application.user.register import Register, RegisterDTO
from app.config import settings
from app.infrastructure.auth.password import PasswordProcessor
from app.infrastructure.gateway.role import RoleGateway
from app.infrastructure.gateway.uow import UnitOfWork
from app.infrastructure.gateway.user import UserGateway


async def create_initial_data(uow: UoW, role_gateway: RoleGateway, create_user: Register) -> None:
    user_role = await role_gateway.get_role_filters(uow, name="user")
    admin_role = await role_gateway.get_role_filters(uow, name="admin")

    if not user_role:
        print("Creating user role")
        await role_gateway.create_role(
            dict(
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
            dict(
                name="admin",
                description="Admin Role",
                permissions=["*"],
            ),
            uow,
        )

    with suppress(HTTPException):
        await create_user(
            RegisterDTO(
                username="admin",
                password=PasswordProcessor().get_password_hash(settings.admin_password.get_secret_value()),
                role_name="admin",
            )
        )
        print("Created admin")
    print("Successfully!")


async def main():
    print("Initializing db...")
    role_gateway = RoleGateway()
    uow = UnitOfWork(session_maker)
    async with uow:
        await create_initial_data(uow, role_gateway, Register(uow, UserGateway(), role_gateway))

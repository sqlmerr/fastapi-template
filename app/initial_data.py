import asyncio

from app.application.create_role import CreateRole
from app.application.schemas.role import RoleCreateSchema

from app.application.common.db import session_maker
from app.adapters.database.uow import UnitOfWork


async def create_initial_data(create_role: CreateRole) -> None:
    try:
        await create_role(
            RoleCreateSchema(
                name="user", description="User role", permissions=["posts:*"]
            )
        )
        await create_role(
            RoleCreateSchema(
                name="admin",
                description="Admin Role",
                permissions=["posts:*", "some_permission"],
            )
        )
    except Exception as e:
        print(e)

#
# async def main() -> None:
#     uow = UnitOfWork(session_maker)
#     async with uow:
#         await cre
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
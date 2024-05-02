
from app.application.create_role import CreateRole
from app.application.schemas.role import RoleCreateSchema


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

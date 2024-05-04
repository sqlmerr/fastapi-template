from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from app.application.create_post import CreatePost
from app.application.delete_post import DeletePost
from app.application.get_all_posts import GetAllPosts
from app.application.get_post import GetPost
from app.application.schemas.post import PostSchema, PostSchemaCreate
from app.application.schemas.user import UserSchema
from app.application.update_post import UpdatePost, UpdatePostDTO
from app.presentation.api.dependencies import get_current_user_with_permissions

router = APIRouter(prefix="/posts", tags=["posts"], route_class=DishkaRoute)


@router.get(
    "/{post_id}",
    dependencies=[Depends(get_current_user_with_permissions(["posts:read"]))],
)
async def get_post(post_id: UUID, interactor: FromDishka[GetPost]) -> PostSchema:
    return await interactor(post_id)


@router.get("/")
async def get_all_posts(
    interactor: FromDishka[GetAllPosts],
    user: Annotated[
        UserSchema, Depends(get_current_user_with_permissions(["posts:read"]))
    ],
) -> list[PostSchema]:
    return await interactor(user.id)


@router.post("/", status_code=201)
async def create_post(
    post: PostSchemaCreate,
    interactor: FromDishka[CreatePost],
    user: Annotated[
        UserSchema, Depends(get_current_user_with_permissions(["posts:create"]))
    ],
):
    result = await interactor(post, user)
    if isinstance(result, bool):
        return {"status": result}
    return {"status": True, "id": result}


@router.delete("/")
async def delete_post(
    post_id: UUID,
    interactor: FromDishka[DeletePost],
    user: Annotated[
        UserSchema, Depends(get_current_user_with_permissions(["posts:delete"]))
    ],
):
    return {"status": await interactor(post_id, user)}


@router.put("/")
async def update_post(
    data: UpdatePostDTO,
    interactor: FromDishka[UpdatePost],
    user: Annotated[
        UserSchema, Depends(get_current_user_with_permissions(["posts:update"]))
    ],
):
    return {"status": await interactor(data, user)}

from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from app.application.common.dto import Pagination
from app.application.post.create_post import CreatePost, CreatePostDTO
from app.application.post.delete_post import DeletePost, DeletePostDTO
from app.application.post.get_all_posts import GetAllPosts
from app.application.post.get_post import GetPost
from app.application.post.update_post import UpdatePost, UpdatePostDTO
from app.application.schemas.post import PostSchema, PostSchemaCreate, PostSchemaUpdate
from app.presentation.api.dependencies import OAuth2Depends

router = APIRouter(prefix="/posts", tags=["posts"], route_class=DishkaRoute)


@router.get("/{post_id}", dependencies=[OAuth2Depends])
async def get_post(post_id: UUID, interactor: FromDishka[GetPost]) -> PostSchema:
    return await interactor(post_id)


@router.get("/", dependencies=[OAuth2Depends])
async def get_all_posts(interactor: FromDishka[GetAllPosts]) -> list[PostSchema]:
    return await interactor(Pagination())


@router.post("/", status_code=201, dependencies=[OAuth2Depends])
async def create_post(
    post: PostSchemaCreate,
    interactor: FromDishka[CreatePost],
):
    result = await interactor(CreatePostDTO(post))
    if isinstance(result, bool):
        return {"status": result}
    return {"status": True, "id": result}


@router.delete("/", dependencies=[OAuth2Depends])
async def delete_post(
    post_id: UUID,
    interactor: FromDishka[DeletePost],
):
    return {"status": await interactor(DeletePostDTO(post_id))}


@router.put("/", dependencies=[OAuth2Depends])
async def update_post(
    data: PostSchemaUpdate,
    interactor: FromDishka[UpdatePost],
):
    return {"status": await interactor(UpdatePostDTO(data))}

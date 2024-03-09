from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.schemas.post import PostSchema, PostSchemaCreate
from app.application.schemas.user import UserSchema
from app.application.update_post import UpdatePostDTO
from app.presentation.interactor_factory import InteractorFactory
from app.presentation.api.dependencies import get_current_user


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/get/", dependencies=[Depends(get_current_user)])
async def get_post(
    post_id: int, ioc: Annotated[InteractorFactory, Depends()]
) -> PostSchema:
    async with ioc.get_post() as interactor:
        return await interactor(post_id)


@router.get("/all/")
async def get_all_posts(
    ioc: Annotated[InteractorFactory, Depends()],
    user: Annotated[UserSchema, Depends(get_current_user)],
) -> list[PostSchema]:
    async with ioc.get_all_posts() as interactor:
        return await interactor(user.id)


@router.post("/create/")
async def create_post(
    post: PostSchemaCreate,
    ioc: Annotated[InteractorFactory, Depends()],
    user: Annotated[UserSchema, Depends(get_current_user)],
):
    async with ioc.create_post() as interactor:
        result = await interactor(post, user)
        if isinstance(result, bool):
            return {"status": True}
        return {"status": True, "id": result}


@router.delete("/delete/")
async def delete_post(
    post_id: int,
    ioc: Annotated[InteractorFactory, Depends()],
    user: Annotated[UserSchema, Depends(get_current_user)],
):
    async with ioc.delete_post() as interactor:
        return {"status": await interactor(post_id, user)}


@router.put("/update/")
async def update_post(
    data: UpdatePostDTO,
    ioc: Annotated[InteractorFactory, Depends()],
    user: Annotated[UserSchema, Depends(get_current_user)],
):
    async with ioc.update_post() as interactor:
        return {"status": await interactor(data, user)}

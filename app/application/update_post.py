from uuid import UUID

from fastapi import HTTPException, status
from pydantic import BaseModel

from app.application.common.interactor import Interactor
from app.application.common.post_gateway import PostReader, PostUpdater
from app.application.common.uow import UoW
from app.application.schemas.post import PostSchemaUpdate
from app.application.schemas.user import UserSchema


class PostReaderAndUpdater(PostReader, PostUpdater):
    pass


class UpdatePostDTO(BaseModel):
    post_id: UUID
    data: PostSchemaUpdate


class UpdatePost(Interactor[UpdatePostDTO, bool]):
    def __init__(self, uow: UoW, post_reader_and_updater: PostReaderAndUpdater) -> None:
        self.uow = uow
        self.post_reader_and_updater = post_reader_and_updater

    async def __call__(self, data: UpdatePostDTO, user: UserSchema) -> bool:
        post = await self.post_reader_and_updater.get_post(data.post_id, self.uow)
        if post is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")
        if post.author_id != user.id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "You don't have access to update this post"
            )
        data_dict = data.data.model_dump(exclude_none=True)
        result = await self.post_reader_and_updater.update_post(
            data.post_id, data_dict, self.uow
        )

        return result

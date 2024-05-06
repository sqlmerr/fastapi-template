from dataclasses import dataclass
from typing import Protocol

from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.post_gateway import PostReader, PostUpdater
from app.application.schemas.post import PostSchemaUpdate
from app.application.schemas.user import UserSchema


class PostReaderAndUpdater(PostReader, PostUpdater, Protocol):
    pass


@dataclass(frozen=True)
class UpdatePostDTO:
    data: PostSchemaUpdate
    user: UserSchema


@dataclass(frozen=True)
class UpdatePost(Interactor[UpdatePostDTO, bool]):
    post_reader_and_updater: PostReaderAndUpdater

    async def __call__(self, data: UpdatePostDTO) -> bool:
        post = await self.post_reader_and_updater.get_post(data.data.id, self.uow)
        if post is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")
        if post.author_id != data.user.id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "You don't have access to update this post"
            )
        data_dict = data.data.model_dump(exclude_none=True)
        result = await self.post_reader_and_updater.update_post(
            data.data.id, data_dict, self.uow
        )

        return result

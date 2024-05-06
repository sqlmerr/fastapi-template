from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.post_gateway import PostDeleter, PostReader
from app.application.schemas.user import UserSchema


class PostReaderAndDeleter(PostReader, PostDeleter, Protocol):
    pass


@dataclass(frozen=True)
class DeletePostDTO:
    post_id: UUID
    user: UserSchema


@dataclass(frozen=True)
class DeletePost(Interactor[DeletePostDTO, bool]):
    post_deleter_and_reader: PostReaderAndDeleter

    async def __call__(self, data: DeletePostDTO) -> bool:
        post = await self.post_deleter_and_reader.get_post(data.post_id, self.uow)
        if post is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")
        if post.author_id != data.user.id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "You don't have access to delete this post"
            )
        result = await self.post_deleter_and_reader.delete_post(data.post_id, self.uow)

        return result

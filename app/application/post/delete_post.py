from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.id_provider import IdProvider
from app.application.common.interactor import Interactor
from app.application.common.post_gateway import PostDeleter, PostReader
from app.application.common.user_gateway import UserReader
from app.domain.exceptions.access import AccessDeniedError
from app.domain.services.access import AccessService


class PostReaderAndDeleter(PostReader, PostDeleter, Protocol):
    pass


@dataclass(frozen=True)
class DeletePostDTO:
    post_id: UUID


@dataclass(frozen=True)
class DeletePost(Interactor[DeletePostDTO, bool]):
    post_deleter_and_reader: PostReaderAndDeleter
    user_reader: UserReader
    id_provider: IdProvider
    access_service: AccessService = field(default_factory=AccessService)

    async def __call__(self, data: DeletePostDTO) -> bool:
        user_id = self.id_provider.get_current_user_id()
        user = await self.user_reader.get_user(user_id, self.uow)
        self.access_service.ensure_has_permissions(user.role_permissions, ["posts:delete"])

        post = await self.post_deleter_and_reader.get_post(data.post_id, self.uow)
        if post is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")
        if post.author_id != user_id:
            raise AccessDeniedError
        result = await self.post_deleter_and_reader.delete_post(data.post_id, self.uow)

        return result

from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.id_provider import IdProvider
from app.application.common.interactor import Interactor
from app.application.common.post_gateway import PostReader, PostUpdater
from app.application.common.user_gateway import UserReader
from app.domain.services.access import AccessService


class PostReaderAndUpdater(PostReader, PostUpdater, Protocol):
    pass


@dataclass(frozen=True)
class UpdatePostDTO:
    id: UUID
    text: str | None = None


@dataclass(frozen=True)
class UpdatePost(Interactor[UpdatePostDTO, bool]):
    post_reader_and_updater: PostReaderAndUpdater
    user_reader: UserReader
    id_provider: IdProvider
    access_service: AccessService = field(default_factory=AccessService)

    async def __call__(self, data: UpdatePostDTO) -> bool:
        user_id = self.id_provider.get_current_user_id()
        user = await self.user_reader.get_user(user_id, self.uow)
        self.access_service.ensure_has_permissions(user.role_permissions, ["posts:update"])

        post = await self.post_reader_and_updater.get_post(data.id, self.uow)
        if post is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")
        if post.author_id != user_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "You don't have access to update this post")

        data_dict = {"id": data.id}
        if data.text:
            data_dict["text"] = data.text
        result = await self.post_reader_and_updater.update_post(data.id, data_dict, self.uow)

        return result

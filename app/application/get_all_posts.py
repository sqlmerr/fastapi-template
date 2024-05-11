from dataclasses import dataclass, field
from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.dto import Pagination
from app.application.common.id_provider import IdProvider
from app.application.common.interactor import Interactor
from app.application.common.post_gateway import PostReader
from app.application.common.user_gateway import UserReader
from app.application.schemas.post import PostSchema
from app.domain.services.access import AccessService


@dataclass(frozen=True)
class GetAllPosts(Interactor[UUID, list[PostSchema]]):
    post_reader: PostReader
    user_reader: UserReader
    id_provider: IdProvider
    access_service: AccessService = field(default_factory=AccessService)

    async def __call__(self, data: Pagination) -> list[PostSchema]:
        user_id = self.id_provider.get_current_user_id()
        user = await self.user_reader.get_user(user_id, self.uow)
        self.access_service.ensure_has_permissions(user.role_permissions, ["posts:read"])

        posts = await self.post_reader.get_all_posts(user_id, self.uow)
        if not posts:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Posts not found")

        return [PostSchema.model_validate(post_db[0], from_attributes=True) for post_db in posts]

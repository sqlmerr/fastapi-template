from dataclasses import dataclass
from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.post_gateway import PostReader
from app.application.schemas.post import PostSchema


@dataclass(frozen=True)
class GetAllPosts(Interactor[UUID, list[PostSchema]]):
    post_reader: PostReader

    async def __call__(self, user_id: UUID) -> list[PostSchema]:
        posts = await self.post_reader.get_all_posts(user_id, self.uow)
        if not posts:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Posts not found")

        return [
            PostSchema.model_validate(post_db[0], from_attributes=True)
            for post_db in posts
        ]

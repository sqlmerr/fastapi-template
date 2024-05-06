from dataclasses import dataclass
from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.post_gateway import PostReader
from app.application.schemas.post import PostSchema


@dataclass(frozen=True)
class GetPost(Interactor[UUID, PostSchema]):
    post_reader: PostReader

    async def __call__(self, data: UUID) -> PostSchema:
        post_db = await self.post_reader.get_post(data, self.uow)
        if post_db is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")

        return PostSchema.model_validate(post_db, from_attributes=True)

from uuid import UUID

from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.post_gateway import PostReader
from app.application.common.uow import UoW
from app.application.schemas.post import PostSchema


class GetAllPosts(Interactor[UUID, list[PostSchema]]):
    def __init__(self, uow: UoW, post_reader: PostReader) -> None:
        self.uow = uow
        self.post_reader = post_reader

    async def __call__(self, user_id: UUID) -> list[PostSchema]:
        posts = await self.post_reader.get_all_posts(user_id, self.uow)
        if not posts:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Posts not found")

        return [
            PostSchema.model_validate(post_db[0], from_attributes=True)
            for post_db in posts
        ]

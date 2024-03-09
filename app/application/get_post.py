from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.schemas.post import PostSchema
from app.application.common.uow import UoW
from app.application.common.post_gateway import PostReader


class GetPost(Interactor[int, PostSchema]):
    def __init__(self, uow: UoW, post_reader: PostReader) -> None:
        self.uow = uow
        self.post_reader = post_reader

    async def __call__(self, data: int) -> PostSchema:
        post_db = await self.post_reader.get_post(data, self.uow)
        if post_db is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")

        return PostSchema.model_validate(post_db, from_attributes=True)

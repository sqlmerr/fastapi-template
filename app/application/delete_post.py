from fastapi import HTTPException, status

from app.application.common.interactor import Interactor
from app.application.common.uow import UoW
from app.application.common.post_gateway import PostDeleter, PostReader
from app.application.schemas.user import UserSchema


class PostReaderAndDeleter(PostReader, PostDeleter):
    pass


class DeletePost(Interactor[int, bool]):
    def __init__(self, uow: UoW, post_deleter_and_reader: PostReaderAndDeleter) -> None:
        self.uow = uow
        self.post_deleter_and_reader = post_deleter_and_reader

    async def __call__(self, data: int, user: UserSchema) -> bool:
        post = await self.post_deleter_and_reader.get_post(data, self.uow)
        if post is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")
        if post.author_id != user.id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "You don't have access to delete this post"
            )
        result = await self.post_deleter_and_reader.delete_post(data, self.uow)

        return result

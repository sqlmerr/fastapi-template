import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from app.adapters.database.post import PostGateway
from app.application.common.uow import UoW
from app.application.common.user_gateway import UserReader
from app.application.create_post import CreatePost, CreatePostDTO
from app.application.get_post import GetPost
from app.application.schemas.post import PostSchema, PostSchemaCreate
from app.application.schemas.user import UserSchema

POST_ID = uuid.uuid4()
USER = UserSchema(
    id=uuid.uuid4(),
    username="tester",
    registered_at=datetime.now(tz=UTC),
    disabled=False,
    role_id=uuid.uuid4(),
)


@pytest.fixture()
def uow() -> UoW:
    uow_mock = AsyncMock()
    uow_mock.commit = AsyncMock()
    uow_mock.flush = AsyncMock()
    uow_mock.rollback = AsyncMock()

    return uow_mock


@pytest.fixture()
def post_gateway() -> PostGateway:
    gateway = AsyncMock()
    gateway.create_post = AsyncMock(return_value=POST_ID)
    gateway.get_post = AsyncMock(return_value=PostSchema(id=POST_ID, text="text", author_id=USER.id))
    return gateway


@pytest.fixture()
def user_gateway() -> UserReader:
    gateway = AsyncMock()
    gateway.get_user = AsyncMock()
    return gateway


async def test_create_post_access(uow, post_gateway, user_gateway):
    interactor = CreatePost(uow=uow, post_creator=post_gateway, user_reader=user_gateway)
    result = await interactor(CreatePostDTO(PostSchemaCreate(text="text"), USER))

    assert result == POST_ID


async def test_get_post_access(uow, post_gateway):
    interactor = GetPost(uow=uow, post_reader=post_gateway)
    result = await interactor(POST_ID)

    assert result == PostSchema(id=POST_ID, text="text", author_id=USER.id)


async def test_get_post_not_found_access(uow):
    post_reader = AsyncMock()
    post_reader.get_post = AsyncMock(return_value=None)
    interactor = GetPost(uow=uow, post_reader=post_reader)

    with pytest.raises(HTTPException):
        await interactor(POST_ID)

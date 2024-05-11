import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import HTTPException

from app.adapters.database.post import PostGateway
from app.application.common.id_provider import IdProvider
from app.application.common.uow import UoW
from app.application.common.user_gateway import UserReader
from app.application.create_post import CreatePost, CreatePostDTO
from app.application.delete_post import DeletePost, DeletePostDTO
from app.application.get_post import GetPost
from app.application.schemas.post import PostSchema, PostSchemaCreate, PostSchemaUpdate
from app.application.update_post import UpdatePost, UpdatePostDTO
from app.domain.exceptions.access import AccessDeniedError

POST_ID = uuid.uuid4()

USER = Mock()
USER.id = uuid.uuid4()
USER.username = "tester"
USER.registered_at = datetime.now(tz=UTC)
USER.disabled = False
USER.role_id = uuid.uuid4()
USER.role_permissions = ["posts:read", "posts:update", "posts:create", "posts:delete", "roles:read"]

USER_NO_ACCESS = Mock()
USER_NO_ACCESS.id = uuid.uuid4()
USER_NO_ACCESS.username = "tester"
USER_NO_ACCESS.registered_at = datetime.now(tz=UTC)
USER_NO_ACCESS.disabled = False
USER_NO_ACCESS.role_id = uuid.uuid4()
USER_NO_ACCESS.role_permissions = []


@pytest.fixture()
def uow() -> UoW:
    uow_mock = AsyncMock()
    uow_mock.commit = AsyncMock()
    uow_mock.flush = AsyncMock()
    uow_mock.rollback = AsyncMock()

    return uow_mock


@pytest.fixture()
def post_gateway() -> PostGateway:
    post = PostSchema(id=POST_ID, text="text", author_id=USER.id)

    gateway = AsyncMock()
    gateway.create_post = AsyncMock(return_value=POST_ID)
    gateway.delete_post = AsyncMock(return_value=True)
    gateway.get_post_by_filters = AsyncMock(return_value=post)
    gateway.get_post = AsyncMock(return_value=post)
    gateway.update_post = AsyncMock(return_value=True)
    return gateway


@pytest.fixture()
def user_gateway() -> UserReader:
    gateway = AsyncMock()
    gateway.get_user = AsyncMock(return_value=USER)
    return gateway


@pytest.fixture()
def user_gateway_no_access() -> UserReader:
    gateway = AsyncMock()
    gateway.get_user = AsyncMock(return_value=USER_NO_ACCESS)
    return gateway


@pytest.fixture()
def id_provider() -> IdProvider:
    id_provider_mock = Mock()
    id_provider_mock.get_current_user_id = Mock(return_value=USER.id)

    return id_provider_mock


async def test_create_post_access(uow, post_gateway, user_gateway, id_provider):
    interactor = CreatePost(uow=uow, post_creator=post_gateway, user_reader=user_gateway, id_provider=id_provider)
    result = await interactor(CreatePostDTO(PostSchemaCreate(text="text")))

    assert result == POST_ID


async def test_create_post_no_access(uow, post_gateway, user_gateway_no_access, id_provider):
    interactor = CreatePost(
        uow=uow, post_creator=post_gateway, user_reader=user_gateway_no_access, id_provider=id_provider
    )

    with pytest.raises(AccessDeniedError):
        await interactor(CreatePostDTO(PostSchemaCreate(text="text")))


async def test_get_post_access(uow, post_gateway, user_gateway, id_provider):
    interactor = GetPost(uow=uow, post_reader=post_gateway, user_reader=user_gateway, id_provider=id_provider)
    result = await interactor(POST_ID)

    assert result == PostSchema(id=POST_ID, text="text", author_id=USER.id)


async def test_get_post_no_access(uow, post_gateway, user_gateway_no_access, id_provider):
    interactor = GetPost(uow=uow, post_reader=post_gateway, user_reader=user_gateway_no_access, id_provider=id_provider)

    with pytest.raises(AccessDeniedError):
        await interactor(POST_ID)


async def test_get_post_not_found(uow, user_gateway, id_provider):
    post_reader = AsyncMock()
    post_reader.get_post = AsyncMock(return_value=None)
    interactor = GetPost(uow=uow, post_reader=post_reader, user_reader=user_gateway, id_provider=id_provider)

    with pytest.raises(HTTPException):
        await interactor(POST_ID)


async def test_delete_post_access(uow, user_gateway, post_gateway, id_provider):
    interactor = DeletePost(
        uow=uow, post_deleter_and_reader=post_gateway, user_reader=user_gateway, id_provider=id_provider
    )
    result = await interactor(DeletePostDTO(POST_ID))

    assert result is True


async def test_delete_post_no_access(uow, user_gateway_no_access, post_gateway, id_provider):
    interactor = DeletePost(
        uow=uow, post_deleter_and_reader=post_gateway, user_reader=user_gateway_no_access, id_provider=id_provider
    )

    with pytest.raises(AccessDeniedError):
        await interactor(DeletePostDTO(POST_ID))


async def test_delete_post_not_found(uow, user_gateway, id_provider):
    post_reader_and_deleter = AsyncMock()
    post_reader_and_deleter.get_post = AsyncMock(return_value=None)
    post_reader_and_deleter.delete_post = AsyncMock()

    interactor = DeletePost(
        uow=uow, post_deleter_and_reader=post_reader_and_deleter, user_reader=user_gateway, id_provider=id_provider
    )

    with pytest.raises(HTTPException):
        await interactor(DeletePostDTO(POST_ID))


async def test_update_post_access(uow, post_gateway, user_gateway, id_provider):
    interactor = UpdatePost(
        uow=uow, post_reader_and_updater=post_gateway, user_reader=user_gateway, id_provider=id_provider
    )
    result = await interactor(UpdatePostDTO(PostSchemaUpdate(id=POST_ID, text="new_text")))

    assert result is True


async def test_update_post_no_access(uow, post_gateway, user_gateway_no_access, id_provider):
    interactor = UpdatePost(
        uow=uow, post_reader_and_updater=post_gateway, user_reader=user_gateway_no_access, id_provider=id_provider
    )

    with pytest.raises(AccessDeniedError):
        await interactor(UpdatePostDTO(PostSchemaUpdate(id=POST_ID, text="new_text")))


async def test_update_post_not_found(uow, user_gateway, id_provider):
    post_reader_and_updater = AsyncMock()
    post_reader_and_updater.get_post = AsyncMock(return_value=None)
    post_reader_and_updater.update_post = AsyncMock()

    interactor = UpdatePost(
        uow=uow, post_reader_and_updater=post_reader_and_updater, user_reader=user_gateway, id_provider=id_provider
    )

    with pytest.raises(HTTPException):
        await interactor(UpdatePostDTO(PostSchemaUpdate(id=POST_ID, text="new_text")))

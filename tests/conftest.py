import pytest

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.application.common.db import session_maker, engine
from fastapi.testclient import TestClient
from httpx import AsyncClient


engine_test = create_async_engine("sqlite+aiosqlite:///db.db")
async_session_maker_test = async_sessionmaker(engine_test)

engine = engine_test  # noqa: F811
session_maker = async_session_maker_test  # noqa: F811

from app.main import create_app  # noqa: E402


app = create_app()
client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

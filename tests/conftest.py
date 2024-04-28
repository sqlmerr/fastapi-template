import pytest

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from httpx import AsyncClient, ASGITransport


from app.main import create_app  # noqa: E402
from app.config import settings
from app.domain.entities.user import User  # noqa: F401
from app.domain.entities.post import Post  # noqa: F401
from app.application.common.db import Base

if settings.test_db_url is None:
    raise ValueError("Please set your test db url in environment variables!")

test_engine = create_async_engine(
    settings.test_db_url.get_secret_value(), poolclass=NullPool
)
test_session_maker = async_sessionmaker(test_engine)

app = create_app(test_session_maker)
# client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
async def db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def session(db) -> AsyncGenerator[AsyncSession, None]:
    async with test_session_maker() as test_session:
        yield test_session


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:
        yield ac
        await ac.aclose()

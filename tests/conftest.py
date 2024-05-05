from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import settings
from app.domain.entities.post import Post  # noqa: F401
from app.domain.entities.user import User  # noqa: F401
from app.main import create_app  # noqa: E402

test_engine = create_async_engine(
    settings.db_url.get_secret_value(), poolclass=NullPool
)
test_session_maker = async_sessionmaker(test_engine)

app = create_app(test_session_maker)
# client = TestClient(app)


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:
        yield ac
        await ac.aclose()

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.core.database import Base


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def test_engine():
    return create_async_engine(TEST_DATABASE_URL, future=True)


@pytest_asyncio.fixture(scope="session")
async def prepare_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def test_session(test_engine, prepare_database):
    async_session = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def client(test_session, monkeypatch):
    async def override_get_session():
        yield test_session

    monkeypatch.setattr("app.core.database.get_session", override_get_session)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_redirect_and_click_increment(client):
    response = await client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200

    data = response.json()
    short_id = data["short_id"]

    redirect_response = await client.get(f"/{short_id}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"].rstrip("/") == "https://example.com"

    stats_response = await client.get(f"/stats/{short_id}")
    assert stats_response.status_code == 200
    assert stats_response.json()["clicks"] == 1

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from main import app
from app.core.database import get_session
from app.models.url import URL
from app.core.database import Base


# Создаём тестовую БД в памяти
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    return engine


@pytest.fixture(scope="session")
async def prepare_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def test_session(test_engine, prepare_database):
    async_session = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


# Подменяем зависимость get_session
@pytest.fixture
def client(test_session, monkeypatch):
    async def override_get_session():
        yield test_session

    monkeypatch.setattr("core.database.get_session", override_get_session)
    return TestClient(app)


def test_redirect_and_click_increment(client):
    # 1. Создаём короткую ссылку
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200

    data = response.json()
    short_id = data["short_id"]

    # 2. Делаем GET /{short_id} -> редирект
    redirect_response = client.get(f"/{short_id}", allow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://example.com"

    # 3. Проверяем статистику
    stats_response = client.get(f"/stats/{short_id}")
    assert stats_response.status_code == 200
    assert stats_response.json()["clicks"] == 1

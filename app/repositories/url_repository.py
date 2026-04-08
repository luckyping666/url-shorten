from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.url import URL


class URLRepository:
    """Repository layer for URL model."""

    async def create(
        self,
        session: AsyncSession,
        short_id: str,
        target_url: str
    ) -> URL:
        url = URL(short_id=short_id, target_url=target_url)
        session.add(url)
        await session.commit()
        await session.refresh(url)
        return url

    async def get_by_short_id(
        self,
        session: AsyncSession,
        short_id: str
    ) -> URL | None:
        stmt = select(URL).where(URL.short_id == short_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def increment_clicks(
        self,
        session: AsyncSession,
        short_id: str
    ) -> None:
        stmt = (
            update(URL)
            .where(URL.short_id == short_id)
            .values(clicks=URL.clicks + 1)
        )
        await session.execute(stmt)
        await session.commit()

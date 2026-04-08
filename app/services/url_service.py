from sqlalchemy.ext.asyncio import AsyncSession
from repositories.url_repository import URLRepository
from utils.short_id import generate_short_id
from models.url import URL


class URLService:
    """Business logic for URL shortening."""

    def __init__(self, repository: URLRepository | None = None):
        self.repository = repository or URLRepository()

    async def create_short_url(
        self,
        session: AsyncSession,
        target_url: str
    ) -> URL:
        """Generate a short ID and save the URL."""
        short_id = generate_short_id()

        # Проверяем, что short_id уникален
        existing = await self.repository.get_by_short_id(session, short_id)
        while existing:
            short_id = generate_short_id()
            existing = await self.repository.get_by_short_id(session, short_id)

        return await self.repository.create(
            session=session,
            short_id=short_id,
            target_url=target_url
        )

    async def resolve_short_url(
        self,
        session: AsyncSession,
        short_id: str
    ) -> str | None:
        """Return original URL and increment click counter."""
        url_obj = await self.repository.get_by_short_id(session, short_id)
        if not url_obj:
            return None

        await self.repository.increment_clicks(session, short_id)
        return url_obj.target_url

    async def get_stats(
        self,
        session: AsyncSession,
        short_id: str
    ) -> int | None:
        """Return number of clicks for a given short_id."""
        url_obj = await self.repository.get_by_short_id(session, short_id)
        if not url_obj:
            return None

        return url_obj.clicks

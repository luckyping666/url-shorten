from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.url_repository import URLRepository
from app.utils.short_id import generate_short_id
from app.models.url import URL


class URLService:
    """
    Сервисный слой для бизнес-логики сокращения URL.

    Отвечает за:
    - генерацию уникальных short_id
    - взаимодействие с репозиторием
    - инкремент счётчиков переходов
    """

    def __init__(self, repository: URLRepository | None = None):
        """
        Инициализация сервиса.

        Args:
            repository (URLRepository | None): Репозиторий для работы с БД.
                Если не передан, создаётся по умолчанию.
        """
        self.repository = repository or URLRepository()

    async def create_short_url(
        self,
        session: AsyncSession,
        target_url: str
    ) -> URL:
        """
        Создаёт сокращённую ссылку.

        Генерирует уникальный short_id и сохраняет URL в базе данных.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            target_url (str): Оригинальный URL.

        Returns:
            URL: Созданный объект URL.
        """
        # Генерируем короткий идентификатор
        short_id = generate_short_id()

        # Проверяем уникальность short_id (защита от коллизий)
        existing = await self.repository.get_by_short_id(session, short_id)
        while existing:
            short_id = generate_short_id()
            existing = await self.repository.get_by_short_id(session, short_id)

        # Приводим URL к строке (на случай, если пришёл HttpUrl)
        return await self.repository.create(
            session=session,
            short_id=short_id,
            target_url=str(target_url)
        )

    async def resolve_short_url(
        self,
        session: AsyncSession,
        short_id: str
    ) -> str | None:
        """
        Возвращает оригинальный URL по short_id и увеличивает счётчик переходов.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            short_id (str): Короткий идентификатор ссылки.

        Returns:
            str | None: Оригинальный URL или None, если ссылка не найдена.
        """
        # Получаем объект URL из базы
        url_obj = await self.repository.get_by_short_id(session, short_id)
        if not url_obj:
            return None

        # Увеличиваем счётчик переходов
        await self.repository.increment_clicks(session, short_id)

        return url_obj.target_url

    async def get_stats(
        self,
        session: AsyncSession,
        short_id: str
    ) -> int | None:
        """
        Возвращает количество переходов по короткой ссылке.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            short_id (str): Короткий идентификатор ссылки.

        Returns:
            int | None: Количество переходов или None, если ссылка не найдена.
        """
        # Получаем объект URL
        url_obj = await self.repository.get_by_short_id(session, short_id)
        if not url_obj:
            return None

        return url_obj.clicks
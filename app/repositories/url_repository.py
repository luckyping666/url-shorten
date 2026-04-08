from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.url import URL


class URLRepository:
    """
    Репозиторий для работы с моделью URL.

    Инкапсулирует всю логику взаимодействия с базой данных
    для сущности URL (создание, получение, обновление).
    """

    async def create(
        self,
        session: AsyncSession,
        short_id: str,
        target_url: str
    ) -> URL:
        """
        Создаёт новую запись URL в базе данных.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            short_id (str): Уникальный короткий идентификатор ссылки.
            target_url (str): Оригинальный URL.

        Returns:
            URL: Созданный объект URL с заполненными полями (включая id).
        """
        # Создаём ORM-объект
        url = URL(short_id=short_id, target_url=target_url)

        # Добавляем в сессию и сохраняем в БД
        session.add(url)
        await session.commit()

        # Обновляем объект, чтобы получить данные из БД (например, id)
        await session.refresh(url)

        return url

    async def get_by_short_id(
        self,
        session: AsyncSession,
        short_id: str
    ) -> URL | None:
        """
        Получает URL по его короткому идентификатору.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            short_id (str): Короткий идентификатор ссылки.

        Returns:
            URL | None: Найденный объект URL или None, если запись отсутствует.
        """
        # Формируем SQL-запрос
        stmt = select(URL).where(URL.short_id == short_id)

        # Выполняем запрос
        result = await session.execute(stmt)

        # Возвращаем одну запись или None
        return result.scalar_one_or_none()

    async def increment_clicks(
        self,
        session: AsyncSession,
        short_id: str
    ) -> None:
        """
        Увеличивает счётчик переходов по короткой ссылке на 1.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            short_id (str): Короткий идентификатор ссылки.

        Returns:
            None
        """
        # Формируем UPDATE-запрос с атомарным увеличением счётчика
        stmt = (
            update(URL)
            .where(URL.short_id == short_id)
            .values(clicks=URL.clicks + 1)
        )

        # Выполняем запрос и фиксируем изменения
        await session.execute(stmt)
        await session.commit()
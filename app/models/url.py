from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func
from app.core.database import Base


class URL(Base):
    """
    Модель таблицы для хранения сокращённых URL.

    Атрибуты:
        id (int): Уникальный идентификатор записи (первичный ключ).
        short_id (str): Короткий идентификатор ссылки (уникальный).
        target_url (str): Исходный (полный) URL, на который происходит редирект.
        clicks (int): Количество переходов по сокращённой ссылке.
        created_at (datetime): Дата и время создания записи.
    """

    __tablename__ = "urls"

    # Первичный ключ, уникальный идентификатор записи
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Короткий ID ссылки (например: abc123), уникальный и индексируемый
    short_id: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        index=True,
        nullable=False
    )

    # Оригинальный URL, на который будет выполняться редирект
    target_url: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # Счётчик переходов по ссылке (по умолчанию 0)
    clicks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    # Дата и время создания записи (устанавливается на стороне БД)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
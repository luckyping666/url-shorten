from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    """
    Схема входящего запроса для создания сокращённой ссылки.

    Атрибуты:
        url (HttpUrl): Валидный URL, который нужно сократить.
    """

    # Оригинальный URL, переданный пользователем (валидируется Pydantic)
    url: HttpUrl


class URLInfo(BaseModel):
    """
    Схема ответа после создания сокращённой ссылки.

    Атрибуты:
        short_id (str): Сгенерированный короткий идентификатор.
        target_url (HttpUrl): Оригинальный URL.
    """

    # Короткий идентификатор ссылки
    short_id: str

    # Оригинальный URL (возвращается в валидированном виде)
    target_url: HttpUrl


class URLStats(BaseModel):
    """
    Схема ответа для получения статистики по ссылке.

    Атрибуты:
        short_id (str): Короткий идентификатор ссылки.
        clicks (int): Количество переходов по ссылке.
    """

    # Короткий идентификатор ссылки
    short_id: str

    # Количество переходов по ссылке
    clicks: int
from app.services.url_service import URLService


def get_url_service() -> URLService:
    return URLService()

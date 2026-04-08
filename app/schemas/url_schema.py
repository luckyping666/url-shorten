from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    """Schema for incoming URL creation request."""
    url: HttpUrl


class URLInfo(BaseModel):
    """Schema returned after creating a short URL."""
    short_id: str
    target_url: HttpUrl


class URLStats(BaseModel):
    """Schema for statistics response."""
    short_id: str
    clicks: int

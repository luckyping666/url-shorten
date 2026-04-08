from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.deps import get_url_service
from app.schemas.url_schema import URLStats
from app.services.url_service import URLService

router = APIRouter()


@router.get("/stats/{short_id}", response_model=URLStats)
async def get_stats(
    short_id: str,
    session: AsyncSession = Depends(get_session),
    service: URLService = Depends(get_url_service)
):
    clicks = await service.get_stats(session, short_id)

    if clicks is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return URLStats(short_id=short_id, clicks=clicks)

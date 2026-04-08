from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from schemas.url import URLStats
from services.url_service import URLService

router = APIRouter()


@router.get("/stats/{short_id}", response_model=URLStats)
async def get_stats(
    short_id: str,
    session: AsyncSession = Depends(get_session),
    service: URLService = Depends(URLService)
):
    clicks = await service.get_stats(session, short_id)

    if clicks is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return URLStats(short_id=short_id, clicks=clicks)

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.deps import get_url_service
from app.schemas.url_schema import URLCreate, URLInfo
from app.services.url_service import URLService

router = APIRouter()


@router.post("/shorten", response_model=URLInfo)
async def create_short_url(
    data: URLCreate,
    session: AsyncSession = Depends(get_session),
    service: URLService = Depends(get_url_service)
):
    url_obj = await service.create_short_url(session, data.url)
    return URLInfo(short_id=url_obj.short_id, target_url=url_obj.target_url)


@router.get("/{short_id}")
async def redirect_to_target(
    short_id: str,
    session: AsyncSession = Depends(get_session),
    service: URLService = Depends(get_url_service)
):
    target_url = await service.resolve_short_url(session, short_id)

    if not target_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=target_url, status_code=307)

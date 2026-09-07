from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.search_repository import SearchRepository
from app.schemas.search import EventSearchResponse
from app.security.dependencies import get_current_user
from app.services.search_service import SearchService


router = APIRouter(prefix="/events")


def get_search_service(
    session: AsyncSession = Depends(get_db),
) -> SearchService:
    repository = SearchRepository(session)
    return SearchService(repository)


@router.get("/search", response_model=EventSearchResponse)
async def search_events(
    q: str = Query(...),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user=Depends(get_current_user),
    service: SearchService = Depends(get_search_service),
):
    try:
        return await service.search_events(
            q=q,
            page=page,
            page_size=page_size,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
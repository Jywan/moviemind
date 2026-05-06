from fastapi import APIRouter
from app.services import analysis as analysis_service

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/genre")
def genre_stats():
    return analysis_service.get_genre_stats()
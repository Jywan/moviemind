from fastapi import APIRouter
from app.services import analysis as analysis_service

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/genre")
def genre_stats():
    return analysis_service.get_genre_stats()

@router.get("/year-trend")
def year_trend():
    return analysis_service.get_year_trend()

@router.get("/top-directors")
def top_directors():
    return analysis_service.get_top_directors()

@router.get("/top-actors")
def top_actors():
    return analysis_service.get_top_actors()
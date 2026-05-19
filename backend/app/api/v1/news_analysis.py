from fastapi import APIRouter, Query

from app.schemas.news_analysis import NewsAnalysisResultsResponse
from app.services.news_analysis_service import NewsAnalysisService

router = APIRouter()
news_analysis_service = NewsAnalysisService()


@router.get("/results", response_model=NewsAnalysisResultsResponse)
async def list_news_analysis_results(limit: int = Query(default=50, ge=1, le=200)):
    return news_analysis_service.list_results(limit=limit)

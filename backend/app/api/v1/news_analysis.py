from fastapi import APIRouter, Query

from app.schemas.news_analysis import NewsAnalysisResultsResponse
from app.services.news_analysis_service import NewsAnalysisService

router = APIRouter()
news_analysis_service = NewsAnalysisService()


@router.get("/results", response_model=NewsAnalysisResultsResponse)
async def list_news_analysis_results(
    page: int = Query(default=1, ge=1, description="当前页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页返回的新闻条数"),
    sort_by: str = Query(default="priority", description="排序字段"),
    sort_dir: str = Query(default="desc", description="排序方向"),
    filter_type: str = Query(default="all", description="影响类型过滤"),
    start_date: str | None = Query(default=None, description="开始日期 (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="结束日期 (YYYY-MM-DD)"),
):
    return news_analysis_service.list_results(
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_dir=sort_dir,
        filter_type=filter_type,
        start_date=start_date,
        end_date=end_date,
    )



from fastapi import APIRouter

from app.schemas.task import ScheduledTaskStatusResponse
from app.services.task_service import TaskService

router = APIRouter()
task_service = TaskService()


@router.get("/news-analysis/status", response_model=ScheduledTaskStatusResponse)
async def get_news_analysis_task_status():
    return task_service.get_news_analysis_status()

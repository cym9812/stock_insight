from fastapi import APIRouter

from backend.schemas.portfolio import PortfolioOverviewResponse
from backend.services.portfolio_service import PortfolioService

router = APIRouter()
portfolio_service = PortfolioService()


@router.get("/overview", response_model=PortfolioOverviewResponse)
async def get_portfolio_overview():
    return portfolio_service.get_overview()

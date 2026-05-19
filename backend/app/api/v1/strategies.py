from fastapi import APIRouter

from app.schemas.strategy import BacktestResponse, RecommendationsResponse
from app.services.strategy_service import StrategyService

router = APIRouter()
strategy_service = StrategyService()


@router.get("/recommendations", response_model=RecommendationsResponse)
async def get_recommendations():
    return strategy_service.get_recommendations()


@router.get("/backtest", response_model=BacktestResponse)
async def get_strategy_backtest(strategy_id: str = "ai_daily"):
    return strategy_service.get_backtest(strategy_id)

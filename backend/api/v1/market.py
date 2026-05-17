from fastapi import APIRouter

from backend.schemas.market import HeatmapItem, MarketIndexItem, MarketSentimentResponse
from backend.services.market_service import MarketService

router = APIRouter()
market_service = MarketService()


@router.get("/sentiment", response_model=MarketSentimentResponse)
async def get_market_sentiment():
    return market_service.get_sentiment()


@router.get("/indices", response_model=list[MarketIndexItem])
async def get_market_indices():
    return market_service.get_indices()


@router.get("/heatmap", response_model=list[HeatmapItem])
async def get_market_heatmap():
    return market_service.get_heatmap()

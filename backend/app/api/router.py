from fastapi import APIRouter

from app.api.v1 import agent, market, news_analysis, portfolio, stocks, strategies, tasks

api_router = APIRouter()
api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(market.router, prefix="/market", tags=["market"])
api_router.include_router(strategies.router, prefix="/strategies", tags=["strategies"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(news_analysis.router, prefix="/news-analysis", tags=["news-analysis"])

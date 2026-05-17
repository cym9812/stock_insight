from fastapi import APIRouter, HTTPException

from backend.schemas.stock import StockAnalysisResponse, StockBarsResponse, StockListResponse
from backend.services.stock_service import StockService

router = APIRouter()
stock_service = StockService()


@router.get("", response_model=StockListResponse)
async def list_stocks():
    try:
        return {"stocks": stock_service.list_stocks()}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/{ticker}/analysis", response_model=StockAnalysisResponse)
async def get_stock_analysis(ticker: str):
    return stock_service.get_stock_analysis(ticker)


@router.get("/{ticker}/bars", response_model=StockBarsResponse)
async def get_stock_bars(ticker: str):
    try:
        return stock_service.get_stock_bars(ticker)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

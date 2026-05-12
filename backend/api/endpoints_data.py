import pandas as pd
from fastapi import APIRouter, HTTPException

from backend.data.storage import FeatureStoreManager

router = APIRouter()
store_manager = FeatureStoreManager()


def dataframe_to_records(df: pd.DataFrame) -> list[dict]:
    """Convert a DataFrame to JSON-safe records for FastAPI responses."""
    if df.empty:
        return []

    safe_df = df.copy()
    for column in safe_df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
        safe_df[column] = safe_df[column].dt.strftime("%Y-%m-%dT%H:%M:%S")

    safe_df = safe_df.astype(object)
    safe_df = safe_df.where(pd.notna(safe_df), None)
    return safe_df.to_dict(orient="records")


@router.get("/stocks")
async def list_stocks():
    """获取本地可用的股票代码列表"""
    try:
        stocks = store_manager.list_stocks()
        return {"stocks": stocks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations")
async def get_recommendations():
    """获取 AI 选股推荐结果 (Mock)"""
    return {
        "date": "2024-05-08",
        "recommendations": [
            {
                "ticker": "AAPL",
                "prediction": "up",
                "confidence": 88,
                "reason": "MACD 金叉，多头排列，且最新季报超预期，模型预测未来一周有 5% 左右涨幅。"
            },
            {
                "ticker": "600519.SH",
                "prediction": "up",
                "confidence": 75,
                "reason": "估值回到历史合理区间，主力资金持续净流入，基本面支撑强劲。"
            },
            {
                "ticker": "TSLA",
                "prediction": "down",
                "confidence": 62,
                "reason": "技术面日线级别顶背离，短期有回调风险，建议观望。"
            }
        ]
    }


@router.get("/market/sentiment")
async def get_market_sentiment():
    """获取市场情绪指数 (Mock)"""
    return {
        "score": 72,
        "label": "Greed",
        "description": "市场情绪偏向乐观，资金活跃度高，主要由科技板块带动。"
    }


@router.get("/market/indices")
async def get_market_indices():
    """获取核心指数概览 (Mock)"""
    return [
        {"name": "Nasdaq", "value": "16,349.10", "change": "+1.2%", "data": [16100, 16200, 16150, 16300, 16349]},
        {"name": "S&P 500", "value": "5,187.67", "change": "+0.5%", "data": [5150, 5160, 5155, 5175, 5187]},
        {"name": "SSE Composite", "value": "3,128.48", "change": "-0.3%", "data": [3150, 3140, 3145, 3130, 3128]}
    ]


@router.get("/market/heatmap")
async def get_market_heatmap():
    """获取板块热力图数据 (Mock)"""
    return [
        {"name": "Technology", "value": 45, "change": 2.5},
        {"name": "Finance", "value": 30, "change": -0.8},
        {"name": "Healthcare", "value": 25, "change": 0.4},
        {"name": "Energy", "value": 20, "change": 1.2},
        {"name": "Consumer", "value": 15, "change": -1.5}
    ]


@router.get("/strategy/backtest")
async def get_strategy_backtest(strategy_id: str = "ai_daily"):
    """获取策略回测表现 (Mock)"""
    return {
        "strategy_id": strategy_id,
        "returns": [100, 102, 101, 105, 108, 107, 112, 115],
        "benchmark": [100, 101, 100, 102, 103, 102, 104, 105],
        "dates": ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08"]
    }


@router.get("/stock/{ticker}/analysis")
async def get_stock_analysis(ticker: str):
    """获取个股深度解析数据 (Mock)"""
    return {
        "ticker": ticker,
        "radar": {
            "indicators": ["Fundamental", "Technical", "Capital", "Sentiment", "Volatility", "Growth"],
            "values": [85, 70, 90, 65, 40, 80]
        },
        "summary": "该股目前处于上升趋势，基本面稳健，主力资金持续流入。建议关注 180 元压力位。",
        "risks": ["行业竞争加剧", "宏观政策变动"]
    }


@router.get("/portfolio/overview")
async def get_portfolio_overview():
    """获取模拟持仓与自选股概览 (Mock)"""
    return {
        "watchlist": [
            {"ticker": "NVDA", "price": 900.23, "change": "+3.5%", "suggestion": "Hold"},
            {"ticker": "BABA", "price": 80.12, "change": "-1.2%", "suggestion": "Buy"},
        ],
        "holdings": [
            {"ticker": "AAPL", "avg_price": 170.5, "current_price": 182.3, "profit_pct": 6.9},
            {"ticker": "TSLA", "avg_price": 200.0, "current_price": 175.4, "profit_pct": -12.3}
        ]
    }


@router.get("/{ticker}")
async def get_stock_data(ticker: str):
    """获取股票历史行情数据 (catch-all, must be last)"""
    try:
        df = store_manager.get_stock_data(ticker)
        return {
            "ticker": ticker,
            "count": len(df),
            "data": dataframe_to_records(df)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

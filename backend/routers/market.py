from fastapi import APIRouter, Query

from services.market_service import get_index_history, get_indices_quote
from services.heatmap_service import get_heatmap_data
from services.stock_service import search_stocks, get_stock_quote, get_stock_history

router = APIRouter()


@router.get("/indices")
def list_indices():
    """取得所有主要指數的即時報價"""
    return get_indices_quote()


@router.get("/indices/{symbol}/history")
def index_history(symbol: str, period: str = Query(default="3mo")):
    """取得單一指數的歷史走勢"""
    return get_index_history(symbol, period)


@router.get("/heatmap")
def heatmap():
    """取得熱力圖資料（依產業分組）"""
    return get_heatmap_data()


@router.get("/search")
def search(q: str = Query(..., min_length=1), limit: int = Query(default=10, le=50)):
    """搜尋股票（模糊比對 ticker 與名稱）"""
    return search_stocks(q, limit)


@router.get("/stocks/{symbol}")
def stock_quote(symbol: str):
    """取得個股即時報價"""
    return get_stock_quote(symbol)


@router.get("/stocks/{symbol}/history")
def stock_history(symbol: str, period: str = Query(default="3mo")):
    """取得個股歷史 K 線"""
    return get_stock_history(symbol, period)

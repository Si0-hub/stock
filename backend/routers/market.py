from fastapi import APIRouter, Query

from services.market_service import get_index_history, get_indices_quote

router = APIRouter()


@router.get("/indices")
def list_indices():
    """取得所有主要指數的即時報價"""
    return get_indices_quote()


@router.get("/indices/{symbol}/history")
def index_history(symbol: str, period: str = Query(default="3mo")):
    """取得單一指數的歷史走勢"""
    return get_index_history(symbol, period)

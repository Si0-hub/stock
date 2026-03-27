import time

import yfinance as yf
from fastapi import HTTPException

from services.heatmap_service import HEATMAP_STOCKS
from services.market_service import INDICES

# 候選池：合併 heatmap 股票與市場指數
STOCK_SEARCH_POOL = [
    {"symbol": s["ticker"], "name": s["name"]}
    for s in HEATMAP_STOCKS
] + [
    {"symbol": symbol, "name": name}
    for symbol, name in INDICES.items()
]

_search_cache: dict = {}
_quote_cache: dict = {}
_history_cache: dict = {}

SEARCH_TTL = 60
QUOTE_TTL = 60
HISTORY_TTL = 300


def _safe_get(obj, attr, default=None):
    try:
        val = getattr(obj, attr, default)
        return val
    except Exception:
        return default


def search_stocks(q: str, limit: int = 10) -> list[dict]:
    cache_key = f"search_{q.lower()}_{limit}"
    now = time.time()
    if cache_key in _search_cache:
        entry = _search_cache[cache_key]
        if (now - entry["timestamp"]) < SEARCH_TTL:
            return entry["data"]

    q_lower = q.lower()

    # 本地候選池模糊搜尋（大小寫不敏感）
    matched = [
        item for item in STOCK_SEARCH_POOL
        if q_lower in item["symbol"].lower() or q_lower in item["name"].lower()
    ]

    results = []
    if matched:
        # 批次取得已知股票的報價
        symbols = [item["symbol"] for item in matched[:limit]]
        tickers_obj = yf.Tickers(" ".join(symbols))
        for item in matched[:limit]:
            symbol = item["symbol"]
            name = item["name"]
            try:
                ticker = tickers_obj.tickers.get(symbol)
                if not ticker:
                    results.append(_build_quote_dict(symbol, name, None))
                    continue
                info = ticker.fast_info
                price = _safe_get(info, "last_price")
                prev_close = _safe_get(info, "previous_close")
                volume = _safe_get(info, "last_volume")
                market_cap = _safe_get(info, "market_cap")

                change = round(price - prev_close, 2) if (price is not None and prev_close is not None) else None
                change_pct = round((change / prev_close) * 100, 2) if (change is not None and prev_close) else None

                results.append({
                    "symbol": symbol,
                    "name": name,
                    "price": round(price, 2) if price is not None else None,
                    "change": change,
                    "changePercent": change_pct,
                    "volume": int(volume) if volume is not None else None,
                    "marketCap": int(market_cap) if market_cap is not None else None,
                })
            except Exception:
                results.append(_build_quote_dict(symbol, name, None))
    else:
        # 嘗試直接用 yfinance 驗證是否為有效 ticker
        try:
            ticker = yf.Ticker(q)
            info = ticker.fast_info
            price = _safe_get(info, "last_price")
            if price is not None:
                prev_close = _safe_get(info, "previous_close")
                volume = _safe_get(info, "last_volume")
                market_cap = _safe_get(info, "market_cap")
                name = ticker.info.get("shortName", q.upper())

                change = round(price - prev_close, 2) if (prev_close is not None) else None
                change_pct = round((change / prev_close) * 100, 2) if (change is not None and prev_close) else None

                results.append({
                    "symbol": q.upper(),
                    "name": name,
                    "price": round(price, 2),
                    "change": change,
                    "changePercent": change_pct,
                    "volume": int(volume) if volume is not None else None,
                    "marketCap": int(market_cap) if market_cap is not None else None,
                })
        except Exception:
            pass

    _search_cache[cache_key] = {"data": results, "timestamp": now}
    return results


def get_stock_quote(symbol: str) -> dict:
    cache_key = symbol.upper()
    now = time.time()
    if cache_key in _quote_cache:
        entry = _quote_cache[cache_key]
        if (now - entry["timestamp"]) < QUOTE_TTL:
            return entry["data"]

    ticker = yf.Ticker(symbol)
    info = ticker.fast_info

    price = _safe_get(info, "last_price")
    prev_close = _safe_get(info, "previous_close")
    volume = _safe_get(info, "last_volume")
    market_cap = _safe_get(info, "market_cap")
    day_high = _safe_get(info, "day_high")
    day_low = _safe_get(info, "day_low")
    year_high = _safe_get(info, "year_high")
    year_low = _safe_get(info, "year_low")

    # 若關鍵欄位都為 None，視為找不到股票
    if price is None and market_cap is None and volume is None:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")

    change = round(price - prev_close, 2) if (price is not None and prev_close is not None) else None
    change_pct = round((change / prev_close) * 100, 2) if (change is not None and prev_close) else None

    name = ticker.info.get("shortName", symbol.upper())

    result = {
        "symbol": symbol.upper(),
        "name": name,
        "price": round(price, 2) if price is not None else None,
        "change": change,
        "changePercent": change_pct,
        "volume": int(volume) if volume is not None else None,
        "marketCap": int(market_cap) if market_cap is not None else None,
        "dayHigh": round(day_high, 2) if day_high is not None else None,
        "dayLow": round(day_low, 2) if day_low is not None else None,
        "fiftyTwoWeekHigh": round(year_high, 2) if year_high is not None else None,
        "fiftyTwoWeekLow": round(year_low, 2) if year_low is not None else None,
    }

    _quote_cache[cache_key] = {"data": result, "timestamp": now}
    return result


def get_stock_history(symbol: str, period: str = "3mo") -> dict:
    cache_key = f"{symbol.upper()}_{period}"
    now = time.time()
    if cache_key in _history_cache:
        entry = _history_cache[cache_key]
        if (now - entry["timestamp"]) < HISTORY_TTL:
            return entry["data"]

    ticker = yf.Ticker(symbol)
    name = ticker.info.get("shortName", symbol.upper())
    df = ticker.history(period=period)
    df.columns = df.columns.str.lower()

    history = []
    for idx, row in df.iterrows():
        history.append(
            {
                "date": idx.strftime("%Y-%m-%d"),
                "open": round(row["open"], 2),
                "high": round(row["high"], 2),
                "low": round(row["low"], 2),
                "close": round(row["close"], 2),
                "volume": int(row["volume"]),
            }
        )

    result = {
        "symbol": symbol.upper(),
        "name": name,
        "history": history,
    }

    _history_cache[cache_key] = {"data": result, "timestamp": now}
    return result


def _build_quote_dict(symbol: str, name: str, _unused) -> dict:
    return {
        "symbol": symbol,
        "name": name,
        "price": None,
        "change": None,
        "changePercent": None,
        "volume": None,
        "marketCap": None,
    }

import yfinance as yf

INDICES = {
    "^GSPC": "S&P 500",
    "^DJI": "道瓊工業指數",
    "^IXIC": "NASDAQ 綜合指數",
    "^SOX": "費城半導體指數",
}


def get_indices_quote() -> list[dict]:
    """取得所有指數的即時報價"""
    results = []
    tickers = yf.Tickers(" ".join(INDICES.keys()))

    for symbol, name in INDICES.items():
        try:
            ticker = tickers.tickers[symbol]
            info = ticker.fast_info
            prev_close = info.previous_close
            price = info.last_price
            change = price - prev_close
            change_pct = (change / prev_close) * 100 if prev_close else 0

            results.append(
                {
                    "symbol": symbol,
                    "name": name,
                    "price": round(price, 2),
                    "change": round(change, 2),
                    "changePercent": round(change_pct, 2),
                }
            )
        except Exception:
            results.append(
                {
                    "symbol": symbol,
                    "name": name,
                    "price": None,
                    "change": None,
                    "changePercent": None,
                }
            )

    return results


def get_index_history(symbol: str, period: str = "3mo") -> dict:
    """取得單一指數的歷史走勢"""
    name = INDICES.get(symbol, symbol)
    ticker = yf.Ticker(symbol)
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

    return {
        "symbol": symbol,
        "name": name,
        "history": history,
    }

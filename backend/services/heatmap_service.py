import time

import yfinance as yf

# 精選美股：涵蓋 11 個 GICS 產業，約 80 檔主要股票
HEATMAP_STOCKS = [
    # Technology 科技
    {"ticker": "AAPL", "name": "Apple", "sector": "科技"},
    {"ticker": "MSFT", "name": "Microsoft", "sector": "科技"},
    {"ticker": "NVDA", "name": "NVIDIA", "sector": "科技"},
    {"ticker": "GOOGL", "name": "Alphabet", "sector": "科技"},
    {"ticker": "META", "name": "Meta", "sector": "科技"},
    {"ticker": "AVGO", "name": "Broadcom", "sector": "科技"},
    {"ticker": "ORCL", "name": "Oracle", "sector": "科技"},
    {"ticker": "CRM", "name": "Salesforce", "sector": "科技"},
    {"ticker": "AMD", "name": "AMD", "sector": "科技"},
    {"ticker": "ADBE", "name": "Adobe", "sector": "科技"},
    {"ticker": "INTC", "name": "Intel", "sector": "科技"},
    {"ticker": "QCOM", "name": "Qualcomm", "sector": "科技"},
    # Consumer Discretionary 非必需消費
    {"ticker": "AMZN", "name": "Amazon", "sector": "非必需消費"},
    {"ticker": "TSLA", "name": "Tesla", "sector": "非必需消費"},
    {"ticker": "HD", "name": "Home Depot", "sector": "非必需消費"},
    {"ticker": "MCD", "name": "McDonald's", "sector": "非必需消費"},
    {"ticker": "NKE", "name": "Nike", "sector": "非必需消費"},
    {"ticker": "SBUX", "name": "Starbucks", "sector": "非必需消費"},
    {"ticker": "BKNG", "name": "Booking", "sector": "非必需消費"},
    {"ticker": "TJX", "name": "TJX Cos", "sector": "非必需消費"},
    # Communication Services 通訊服務
    {"ticker": "GOOG", "name": "Alphabet C", "sector": "通訊服務"},
    {"ticker": "NFLX", "name": "Netflix", "sector": "通訊服務"},
    {"ticker": "DIS", "name": "Disney", "sector": "通訊服務"},
    {"ticker": "CMCSA", "name": "Comcast", "sector": "通訊服務"},
    {"ticker": "TMUS", "name": "T-Mobile", "sector": "通訊服務"},
    {"ticker": "VZ", "name": "Verizon", "sector": "通訊服務"},
    # Healthcare 醫療保健
    {"ticker": "UNH", "name": "UnitedHealth", "sector": "醫療保健"},
    {"ticker": "JNJ", "name": "Johnson & Johnson", "sector": "醫療保健"},
    {"ticker": "LLY", "name": "Eli Lilly", "sector": "醫療保健"},
    {"ticker": "ABBV", "name": "AbbVie", "sector": "醫療保健"},
    {"ticker": "MRK", "name": "Merck", "sector": "醫療保健"},
    {"ticker": "PFE", "name": "Pfizer", "sector": "醫療保健"},
    {"ticker": "TMO", "name": "Thermo Fisher", "sector": "醫療保健"},
    {"ticker": "ABT", "name": "Abbott", "sector": "醫療保健"},
    # Financials 金融
    {"ticker": "BRK-B", "name": "Berkshire B", "sector": "金融"},
    {"ticker": "JPM", "name": "JPMorgan", "sector": "金融"},
    {"ticker": "V", "name": "Visa", "sector": "金融"},
    {"ticker": "MA", "name": "Mastercard", "sector": "金融"},
    {"ticker": "BAC", "name": "Bank of America", "sector": "金融"},
    {"ticker": "WFC", "name": "Wells Fargo", "sector": "金融"},
    {"ticker": "GS", "name": "Goldman Sachs", "sector": "金融"},
    {"ticker": "MS", "name": "Morgan Stanley", "sector": "金融"},
    # Industrials 工業
    {"ticker": "GE", "name": "GE Aerospace", "sector": "工業"},
    {"ticker": "CAT", "name": "Caterpillar", "sector": "工業"},
    {"ticker": "UNP", "name": "Union Pacific", "sector": "工業"},
    {"ticker": "RTX", "name": "RTX Corp", "sector": "工業"},
    {"ticker": "HON", "name": "Honeywell", "sector": "工業"},
    {"ticker": "BA", "name": "Boeing", "sector": "工業"},
    {"ticker": "DE", "name": "Deere & Co", "sector": "工業"},
    {"ticker": "LMT", "name": "Lockheed Martin", "sector": "工業"},
    # Consumer Staples 必需消費
    {"ticker": "PG", "name": "Procter & Gamble", "sector": "必需消費"},
    {"ticker": "KO", "name": "Coca-Cola", "sector": "必需消費"},
    {"ticker": "PEP", "name": "PepsiCo", "sector": "必需消費"},
    {"ticker": "COST", "name": "Costco", "sector": "必需消費"},
    {"ticker": "WMT", "name": "Walmart", "sector": "必需消費"},
    {"ticker": "PM", "name": "Philip Morris", "sector": "必需消費"},
    {"ticker": "CL", "name": "Colgate", "sector": "必需消費"},
    # Energy 能源
    {"ticker": "XOM", "name": "Exxon Mobil", "sector": "能源"},
    {"ticker": "CVX", "name": "Chevron", "sector": "能源"},
    {"ticker": "COP", "name": "ConocoPhillips", "sector": "能源"},
    {"ticker": "SLB", "name": "Schlumberger", "sector": "能源"},
    {"ticker": "EOG", "name": "EOG Resources", "sector": "能源"},
    {"ticker": "MPC", "name": "Marathon Petro", "sector": "能源"},
    # Utilities 公用事業
    {"ticker": "NEE", "name": "NextEra Energy", "sector": "公用事業"},
    {"ticker": "DUK", "name": "Duke Energy", "sector": "公用事業"},
    {"ticker": "SO", "name": "Southern Co", "sector": "公用事業"},
    {"ticker": "D", "name": "Dominion Energy", "sector": "公用事業"},
    {"ticker": "AEP", "name": "American Electric", "sector": "公用事業"},
    # Real Estate 不動產
    {"ticker": "PLD", "name": "Prologis", "sector": "不動產"},
    {"ticker": "AMT", "name": "American Tower", "sector": "不動產"},
    {"ticker": "EQIX", "name": "Equinix", "sector": "不動產"},
    {"ticker": "SPG", "name": "Simon Property", "sector": "不動產"},
    {"ticker": "O", "name": "Realty Income", "sector": "不動產"},
    # Materials 原物料
    {"ticker": "LIN", "name": "Linde", "sector": "原物料"},
    {"ticker": "APD", "name": "Air Products", "sector": "原物料"},
    {"ticker": "SHW", "name": "Sherwin-Williams", "sector": "原物料"},
    {"ticker": "FCX", "name": "Freeport-McMoRan", "sector": "原物料"},
    {"ticker": "NEM", "name": "Newmont", "sector": "原物料"},
]

_cache: dict = {"data": None, "timestamp": 0}
CACHE_TTL = 300  # 5 分鐘快取


def get_heatmap_data() -> list[dict]:
    """取得熱力圖資料：依產業分組，包含市值與漲跌幅"""
    now = time.time()
    if _cache["data"] and (now - _cache["timestamp"]) < CACHE_TTL:
        return _cache["data"]

    tickers_list = [s["ticker"] for s in HEATMAP_STOCKS]
    tickers_str = " ".join(tickers_list)

    # 用 download 批次取得近 2 天收盤價計算漲跌幅
    df = yf.download(tickers_str, period="5d", group_by="ticker", threads=True)

    # 取得市值
    tickers_obj = yf.Tickers(tickers_str)

    # 建立 ticker -> stock info 的對照表
    stock_map = {s["ticker"]: s for s in HEATMAP_STOCKS}

    sectors: dict[str, list[dict]] = {}
    for ticker in tickers_list:
        try:
            ticker_df = df[ticker]
            closes = ticker_df["Close"].dropna()
            if len(closes) < 2:
                continue
            prev_close = float(closes.iloc[-2])
            last_close = float(closes.iloc[-1])
            change_pct = ((last_close - prev_close) / prev_close) * 100

            # 取市值，若失敗則跳過
            t_obj = tickers_obj.tickers.get(ticker)
            if not t_obj:
                continue
            market_cap = t_obj.fast_info["market_cap"]
            if not market_cap or market_cap <= 0:
                continue

            info = stock_map[ticker]
            sector_name = info["sector"]
            if sector_name not in sectors:
                sectors[sector_name] = []
            sectors[sector_name].append(
                {
                    "ticker": ticker,
                    "name": info["name"],
                    "marketCap": int(market_cap),
                    "changePercent": round(change_pct, 2),
                    "price": round(last_close, 2),
                }
            )
        except Exception:
            continue

    result = []
    for sector_name, stocks in sectors.items():
        result.append({"name": sector_name, "children": stocks})

    _cache["data"] = result
    _cache["timestamp"] = now
    return result

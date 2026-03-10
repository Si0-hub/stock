from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import market

app = FastAPI(title="StockAnalyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market.router, prefix="/api/market", tags=["market"])


@app.get("/")
def root():
    return {"message": "StockAnalyzer API is running"}

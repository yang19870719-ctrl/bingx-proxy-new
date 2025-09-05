from fastapi import FastAPI
from bingx import get_price

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "BingX Proxy API is running"}

@app.get("/price")
def price(symbol: str = "BTCUSDT", interval: str = "1h"):
    """取得 BingX 即時價格或 K 線"""
    return get_price(symbol, interval)

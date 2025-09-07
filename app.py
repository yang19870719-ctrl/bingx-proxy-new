from fastapi import FastAPI, Query
from typing import List, Dict
from bingx import get_price, get_klines

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "BingX Proxy API is running"}

@app.get("/price")
def price(symbol: str):
    p = get_price(symbol)
    return {"symbol": symbol, "price": p}

@app.get("/klines")
def klines(symbol: str, interval: str = "1h", limit: int = 200):
    ks = get_klines(symbol, interval, limit)
    return {"symbol": symbol, "interval": interval, "klines": ks}

@app.get("/bundle")
def bundle(
    symbols: str = Query(..., description="如: BTCUSDT,ETHUSDT,BNBUSDT"),
    intervals: str = Query("1h,4h"),
    limit: int = 200
):
    syms = [s.strip() for s in symbols.split(",") if s.strip()]
    ivals = [i.strip() for i in intervals.split(",") if i.strip()]
    out: Dict[str, Dict] = {}
    for s in syms:
        p = get_price(s)
        out[s] = {"price": p, "klines": {}}
        for iv in ivals:
            out[s]["klines"][iv] = get_klines(s, iv, limit)
    return {"timestamp": __import__("time").time()*1000, "symbols": out}

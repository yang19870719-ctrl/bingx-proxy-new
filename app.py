from fastapi import FastAPI, Query
from typing import Dict, List
from bingx import get_swap_price, get_swap_klines
import time

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "BingX Proxy API is running"}

@app.get("/price")
def price(symbol: str):
    p = get_swap_price(symbol)
    return {"symbol": symbol, "price": p}

@app.get("/klines")
def klines(symbol: str, interval: str = "1h", limit: int = 200):
    ks = get_swap_klines(symbol, interval, limit)
    return {"symbol": symbol, "interval": interval, "klines": ks}

@app.get("/bundle")
def bundle(
    symbols: str = Query("BTCUSDT,ETHUSDT,BNBUSDT"),
    intervals: str = Query("1h,4h"),
    limit: int = 200
):
    syms = [s.strip() for s in symbols.split(",") if s.strip()]
    ivals = [i.strip() for i in intervals.split(",") if i.strip()]
    out: Dict[str, Dict] = {}
    for s in syms:
        out[s] = {
            "price": get_swap_price(s),
            "klines": {iv: get_swap_klines(s, iv, limit) for iv in ivals}
        }
    return {"timestamp": int(time.time() * 1000), "symbols": out}

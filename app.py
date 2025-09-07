import requests, time
from fastapi import FastAPI
from typing import Dict, List

app = FastAPI()
BASE_URL = "https://open-api.bingx.com"

def get_price(symbol: str) -> float:
    url = f"{BASE_URL}/openApi/swap/v2/quote/price"
    r = requests.get(url, params={"symbol": symbol}, timeout=10).json()
    if r.get("code") == 0 and "data" in r and "price" in r["data"]:
        return float(r["data"]["price"])
    return None

def get_klines(symbol: str, interval: str, limit: int) -> List[Dict]:
    url = f"{BASE_URL}/openApi/swap/v2/quote/klines"
    r = requests.get(url, params={"symbol": symbol, "interval": interval, "limit": limit}, timeout=10).json()
    if r.get("code") == 0 and "data" in r:
        return r["data"]
    return []

@app.get("/")
def root():
    return {"msg": "BingX Proxy API is running"}

@app.get("/bundle")
def bundle(symbols: str = "BTCUSDT,ETHUSDT,BNBUSDT", intervals: str = "1h,4h", limit: int = 200):
    t = int(time.time() * 1000)
    out = {}
    for s in symbols.split(","):
        s = s.strip()
        if not s: continue
        out[s] = {
            "price": get_price(s),
            "klines": {iv: get_klines(s, iv, limit) for iv in intervals.split(",")}
        }
    return {"timestamp": t, "symbols": out}

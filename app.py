import time, requests
from typing import List, Dict

BASE_URL = "https://open-api.bingx.com"

def _get_json(url: str, params: dict) -> dict:
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data.get("data", data)

def _spot_price(symbol: str) -> float:
    url = f"{BASE_URL}/openApi/spot/v1/ticker/price"
    data = _get_json(url, {"symbol": symbol})
    price = data.get("price") if isinstance(data, dict) else None
    return float(price) if price is not None else None

def _spot_klines(symbol: str, interval: str, limit: int) -> List[Dict]:
    url = f"{BASE_URL}/openApi/spot/v1/market/kline"
    raw = _get_json(url, {"symbol": symbol, "interval": interval, "limit": limit})
    out = []
    for row in raw if isinstance(raw, list) else []:
        o, h, l, c, v = map(float, [row[1], row[2], row[3], row[4], row[5]])
        out.append({
            "openTime": int(row[0]),
            "open": o, "high": h, "low": l, "close": c,
            "volume": v,
            "closeTime": int(row[6]) if len(row) > 6 else None
        })
    return out

@app.get("/bundle")
def bundle(
    symbols: str = "BTCUSDT,ETHUSDT,BNBUSDT",
    intervals: str = "1h,4h",
    limit: int = 200
):
    t = int(time.time() * 1000)
    sym_list = [s.strip() for s in symbols.split(",") if s.strip()]
    intv_list = [i.strip() for i in intervals.split(",") if i.strip()]

    result = {"timestamp": t, "symbols": {}}

    for sym in sym_list:
        item = {"price": _spot_price(sym), "klines": {}}
        for iv in intv_list:
            try:
                item["klines"][iv] = _spot_klines(sym, iv, limit)
            except Exception as e:
                item["klines"][iv] = {"error": str(e)}
        result["symbols"][sym] = item

    return result

import requests

BASE_URL = "https://open-api.bingx.com"

def get_price(symbol="BTCUSDT", interval="1h"):
    url = f"{BASE_URL}/openApi/swap/v2/quote/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 1
    }
    res = requests.get(url, params=params, timeout=10)
    if res.status_code == 200:
        data = res.json()
        return {"symbol": symbol, "kline": data.get("data", [])}
    else:
        return {"error": res.text}

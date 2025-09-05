import requests

BASE_URL = "https://open-api.bingx.com"

def get_price(symbol="BTCUSDT"):
    url = f"{BASE_URL}/openApi/spot/v1/ticker/price"
    params = {"symbol": symbol}
    res = requests.get(url, params=params, timeout=10)
    if res.status_code == 200:
        data = res.json()
        return {
            "symbol": data.get("data", {}).get("symbol", symbol),
            "price": data.get("data", {}).get("price")
        }
    else:
        return {"error": res.text}


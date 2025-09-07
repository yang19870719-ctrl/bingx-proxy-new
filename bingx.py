import os, time, hmac, hashlib, requests
from typing import Dict, Any, Optional

PUBLIC_BASE = "https://open-api.bingx.com"
TIMEOUT = 8
RETRIES = 2

API_KEY = os.getenv("BINGX_API_KEY", "")
SECRET  = os.getenv("BINGX_SECRET_KEY", "")

def _get(url: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """GET with small retry"""
    for _ in range(RETRIES):
        try:
            r = requests.get(url, params=params, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
        except Exception:
            time.sleep(0.3)
    return None

def _signed_get(path: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """BingX 簽名 GET（若你要走需要簽名的行情/交易端點）"""
    if not API_KEY or not SECRET:
        return None
    ts = str(int(time.time() * 1000))
    params.update({"timestamp": ts})
    # 注意：不同 BingX 路徑簽名字串格式可能略有差異，以下是常見 queryString 直接 HMAC-SHA256
    query = "&".join([f"{k}={params[k]}" for k in sorted(params)])
    sign  = hmac.new(SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    headers = {"X-BX-APIKEY": API_KEY}
    url = f"{PUBLIC_BASE}{path}?{query}&signature={sign}"
    for _ in range(RETRIES):
        try:
            r = requests.get(url, headers=headers, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
        except Exception:
            time.sleep(0.3)
    return None

def get_price(symbol: str) -> Optional[float]:
    """
    先試公有：/openApi/swap/v2/quote/price
    回傳格式示例：{"code":0,"data":{"symbol":"BTCUSDT","price":"110800.01"}}
    """
    pub = _get(f"{PUBLIC_BASE}/openApi/swap/v2/quote/price", {"symbol": symbol})
    if pub and pub.get("data") and pub["data"].get("price"):
        try:
            return float(pub["data"]["price"])
        except Exception:
            pass

    # 備援：若一定要用簽名端點（你的帳戶可能要求）
    signed = _signed_get("/openApi/swap/v2/quote/price", {"symbol": symbol})
    if signed and signed.get("data") and signed["data"].get("price"):
        try:
            return float(signed["data"]["price"])
        except Exception:
            pass
    return None

def get_klines(symbol: str, interval: str, limit: int = 200) -> list:
    """
    公有：/openApi/swap/v2/quote/klines
    參考回傳：{"code":0,"data":[[openTime,open,high,low,close,volume,closeTime],...]}
    """
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    data = _get(f"{PUBLIC_BASE}/openApi/swap/v2/quote/klines", params)
    if data and isinstance(data.get("data"), list):
        return data["data"]

    # 備援（簽名）
    data = _signed_get("/openApi/swap/v2/quote/klines", params)
    if data and isinstance(data.get("data"), list):
        return data["data"]
    return []

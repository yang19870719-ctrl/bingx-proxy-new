import time, requests
from typing import Any, Dict, Optional, List

PUBLIC_BASE = "https://open-api.bingx.com"
TIMEOUT = 8
RETRIES = 2

def _get(url: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for _ in range(RETRIES):
        try:
            r = requests.get(url, params=params, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
        except Exception:
            time.sleep(0.25)
    return None

def get_swap_price(symbol: str) -> Optional[float]:
    """
    U本位合約行情（公共端點，無需簽名）:
    /openApi/swap/v2/quote/price -> {"code":0,"data":{"symbol":"BTCUSDT","price":"110800.01"}}
    """
    data = _get(f"{PUBLIC_BASE}/openApi/swap/v2/quote/price", {"symbol": symbol})
    try:
        if data and data.get("code") == 0 and data.get("data") and data["data"].get("price"):
            return float(data["data"]["price"])
    except Exception:
        pass
    return None

def get_swap_klines(symbol: str, interval: str, limit: int = 200) -> List[list]:
    """
    /openApi/swap/v2/quote/klines -> {"code":0,"data":[[openTime,open,high,low,close,volume,closeTime], ...]}
    """
    data = _get(f"{PUBLIC_BASE}/openApi/swap/v2/quote/klines",
                {"symbol": symbol, "interval": interval, "limit": limit})
    if data and data.get("code") == 0 and isinstance(data.get("data"), list):
        return data["data"]
    return []

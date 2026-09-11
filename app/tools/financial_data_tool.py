from datetime import datetime, timezone
from typing import Any

import httpx


class FinancialDataTool:
    """Fetch current/most-recent market quote data from Alpha Vantage."""

    name = "external_financial_data"
    base_url = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str, timeout: float = 10.0):
        if not api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY is missing. Add it to your .env file.")
        self.api_key = api_key
        self.timeout = timeout

    def get_quote(self, symbol: str) -> dict[str, Any]:
        symbol = symbol.strip().upper()
        if not symbol:
            raise ValueError("Stock symbol cannot be empty.")

        response = httpx.get(
            self.base_url,
            params={
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": self.api_key,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()

        if "Error Message" in payload:
            raise ValueError(payload["Error Message"])
        if "Note" in payload:
            raise RuntimeError(payload["Note"])

        quote = payload.get("Global Quote", {})
        if not quote or not quote.get("05. price"):
            raise ValueError(f"No quote data returned for symbol '{symbol}'.")

        return {
            "symbol": quote.get("01. symbol", symbol),
            "price": float(quote["05. price"]),
            "change": float(quote.get("09. change", 0) or 0),
            "change_percent": quote.get("10. change percent", ""),
            "latest_trading_day": quote.get("07. latest trading day"),
            "source": "Alpha Vantage",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
        }

    def run(self, symbol: str) -> dict[str, Any]:
        quote = self.get_quote(symbol)
        return {
            "tool": self.name,
            "operation": "global_quote",
            "status": "success",
            "data": quote,
        }

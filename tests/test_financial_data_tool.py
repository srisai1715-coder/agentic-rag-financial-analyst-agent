import pytest

from app.tools.financial_data_tool import FinancialDataTool


def test_financial_data_tool_requires_api_key():
    with pytest.raises(ValueError):
        FinancialDataTool("")


def test_financial_data_tool_parses_quote(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "Global Quote": {
                    "01. symbol": "MSFT",
                    "05. price": "510.25",
                    "09. change": "2.50",
                    "10. change percent": "0.49%",
                    "07. latest trading day": "2026-09-04",
                }
            }

    def fake_get(*args, **kwargs):
        assert kwargs["params"]["function"] == "GLOBAL_QUOTE"
        assert kwargs["params"]["symbol"] == "MSFT"
        return FakeResponse()

    monkeypatch.setattr("app.tools.financial_data_tool.httpx.get", fake_get)

    result = FinancialDataTool("test-key").run("msft")
    assert result["status"] == "success"
    assert result["data"]["symbol"] == "MSFT"
    assert result["data"]["price"] == 510.25
    assert result["data"]["source"] == "Alpha Vantage"


def test_financial_data_tool_rejects_missing_quote(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"Global Quote": {}}

    monkeypatch.setattr(
        "app.tools.financial_data_tool.httpx.get",
        lambda *args, **kwargs: FakeResponse(),
    )

    with pytest.raises(ValueError):
        FinancialDataTool("test-key").run("MSFT")

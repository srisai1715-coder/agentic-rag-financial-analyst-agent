from app.agent.graph import route_question, extract_msft_symbol


def test_routes_stock_price_to_external_data():
    result = route_question({"user_query": "What is Microsoft's current stock price?"})
    assert result["route"] == "external_data"


def test_extracts_microsoft_symbol():
    assert extract_msft_symbol("What is MSFT share price?") == "MSFT"


def test_rejects_unknown_company_symbol():
    try:
        extract_msft_symbol("What is Apple's stock price?")
    except ValueError as exc:
        assert "supported stock symbol" in str(exc)
    else:
        raise AssertionError("Expected ValueError")

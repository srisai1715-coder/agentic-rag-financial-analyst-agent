from app.tools.risk_tool import RiskAnalysisTool


def test_risk_tool_detects_categories():
    tool = RiskAnalysisTool()
    result = tool.run(
        [
            {
                "text": "Microsoft faces cybersecurity threats and increasing competition.",
                "metadata": {"page": 10},
            }
        ]
    )

    assert result["tool"] == "risk_analysis"
    assert result["risk_count"] == 1
    assert "cybersecurity" in result["categories"]
    assert "competition" in result["categories"]


def test_risk_tool_ignores_irrelevant_evidence():
    tool = RiskAnalysisTool()
    result = tool.run(
        [
            {
                "text": "Revenue was $281.7 billion in fiscal year 2025.",
                "metadata": {"page": 72},
            }
        ]
    )

    assert result["risk_count"] == 0
    assert result["categories"] == []
    assert result["risks"] == []


def test_risk_tool_preserves_page_source():
    tool = RiskAnalysisTool()
    result = tool.run(
        [
            {
                "text": "We face risks related to regulatory requirements and privacy.",
                "metadata": {"page": 35},
            }
        ]
    )

    assert result["risks"][0]["source"] == "p. 35"

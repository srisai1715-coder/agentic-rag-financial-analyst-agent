from app.agent.trace import build_tool_trace


def test_tool_trace_adds_step_numbers():
    result = build_tool_trace(
        [
            {"tool": "annual_report_rag", "query": "revenue"},
            {"tool": "financial_calculation", "operation": "revenue_growth"},
            {"tool": "verification", "status": "passed"},
        ]
    )

    assert result == [
        {"step": 1, "tool": "annual_report_rag", "query": "revenue"},
        {"step": 2, "tool": "financial_calculation", "operation": "revenue_growth"},
        {"step": 3, "tool": "verification", "status": "passed"},
    ]


def test_tool_trace_handles_empty_calls():
    assert build_tool_trace([]) == []


def test_tool_trace_ignores_unknown_extra_fields():
    result = build_tool_trace([{"tool": "risk_analysis", "extra": "internal"}])
    assert result == [{"step": 1, "tool": "risk_analysis"}]

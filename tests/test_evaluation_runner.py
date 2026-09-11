from evaluation.evaluate import evaluate_items


def test_evaluate_items_handles_multiple_results():
    items = [
        {
            "id": "q1",
            "question": "Revenue?",
            "expected_answer_contains": ["281.724"],
        },
        {
            "id": "q2",
            "question": "Growth?",
            "expected_answer_contains": ["14.93", "%"],
            "expected_tool": "financial_calculation",
        },
    ]

    results = [
        {
            "answer": "Revenue was 281.724 billion.",
            "tool_calls": [{"tool": "annual_report_rag"}],
            "verification": {"verified": True},
        },
        {
            "answer": "Growth was 14.93%.",
            "tool_calls": [{"tool": "financial_calculation"}],
            "verification": {"verified": True},
        },
    ]

    summary = evaluate_items(items, results)

    assert summary["passed"] == 2
    assert summary["total"] == 2
    assert summary["pass_rate"] == 1.0

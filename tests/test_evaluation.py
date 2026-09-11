from evaluation.evaluate import evaluate_items, load_dataset


def test_dataset_loads():
    dataset = load_dataset()

    assert len(dataset) == 5
    assert dataset[0]["id"] == "q1"


def test_evaluate_verified_result():
    items = [
        {
            "id": "q1",
            "question": "Revenue?",
            "expected_answer_contains": ["281.724", "billion"],
        }
    ]

    results = [
        {
            "answer": "Microsoft reported revenue of $281.724 billion.",
            "tool_calls": [{"tool": "annual_report_rag"}],
            "verification": {"verified": True},
        }
    ]

    summary = evaluate_items(items, results)

    assert summary["passed"] == 1
    assert summary["total"] == 1
    assert summary["pass_rate"] == 1.0


def test_evaluate_fails_when_unverified():
    items = [
        {
            "id": "q1",
            "question": "Revenue?",
            "expected_answer_contains": ["281.724"],
        }
    ]

    results = [
        {
            "answer": "Microsoft reported revenue of $281.724 billion.",
            "verification": {"verified": False},
        }
    ]

    summary = evaluate_items(items, results)

    assert summary["passed"] == 0
    assert summary["pass_rate"] == 0.0


def test_evaluate_checks_expected_tool():
    items = [
        {
            "id": "q3",
            "question": "Revenue growth?",
            "expected_tool": "financial_calculation",
        }
    ]

    good = evaluate_items(
        items,
        [
            {
                "answer": "Revenue growth was 14.93%.",
                "tool_calls": [{"tool": "financial_calculation"}],
                "verification": {"verified": True},
            }
        ],
    )
    assert good["passed"] == 1

    bad = evaluate_items(
        items,
        [
            {
                "answer": "Revenue growth was 14.93%.",
                "tool_calls": [{"tool": "annual_report_rag"}],
                "verification": {"verified": True},
            }
        ],
    )
    assert bad["passed"] == 0

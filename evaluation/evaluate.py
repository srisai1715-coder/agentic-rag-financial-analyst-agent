import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "evaluation" / "dataset.json"


def load_dataset() -> list[dict[str, Any]]:
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_result(item: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    answer = str(result.get("answer", "")).lower()

    answer_checks = [
        str(expected).lower() in answer
        for expected in item.get("expected_answer_contains", [])
    ]
    answer_pass = all(answer_checks) if answer_checks else True

    expected_tool = item.get("expected_tool")
    tool_calls = result.get("tool_calls", [])
    tool_names = {call.get("tool") for call in tool_calls}
    tool_pass = expected_tool is None or expected_tool in tool_names

    verification = result.get("verification") or {}
    verification_pass = verification.get("verified") is True

    passed = answer_pass and tool_pass and verification_pass

    return {
        "id": item["id"],
        "question": item["question"],
        "passed": passed,
        "answer_check": answer_pass,
        "tool_check": tool_pass,
        "verification_check": verification_pass,
    }


def evaluate_items(
    items: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    evaluated = [
        evaluate_result(item, result)
        for item, result in zip(items, results)
    ]

    passed = sum(item["passed"] for item in evaluated)
    total = len(evaluated)

    return {
        "passed": passed,
        "total": total,
        "pass_rate": (passed / total) if total else 0.0,
        "results": evaluated,
    }


def run_agent_evaluation() -> dict[str, Any]:
    """Run the dataset through the local agent and evaluate every result."""
    from app.agent.graph import build_graph

    dataset = load_dataset()
    graph = build_graph()
    results = []

    for item in dataset:
        result = graph.invoke({"user_query": item["question"]})
        results.append(
            {
                "answer": result.get("final_answer", ""),
                "tool_calls": result.get("tool_calls", []),
                "verification": result.get("verification", {}),
            }
        )

    return evaluate_items(dataset, results)


if __name__ == "__main__":
    summary = run_agent_evaluation()

    print(
        f"Evaluation: {summary['passed']}/{summary['total']} passed "
        f"({summary['pass_rate']:.0%})"
    )

    for item in summary["results"]:
        status = "PASS" if item["passed"] else "FAIL"
        print(f"{status} {item['id']}: {item['question']}")

    if summary["passed"] != summary["total"]:
        raise SystemExit(1)

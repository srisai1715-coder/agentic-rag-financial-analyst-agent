from typing import Any, TypedDict

class AgentState(TypedDict, total=False):
    user_query: str
    tool_calls: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    sources: list[str]
    calculation: dict[str, Any]
    ratio: dict[str, Any]
    risk_analysis: dict[str, Any]
    verification: dict[str, Any]
    final_answer: str
    route: str
    external_data: dict[str, Any]

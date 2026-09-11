import os
from typing import Any


DEFAULT_LANGSMITH_ENDPOINT = "https://api.smith.langchain.com"
DEFAULT_PROJECT = "financial-analyst-agent"


def is_langsmith_tracing_enabled() -> bool:
    """Return whether LangSmith tracing is enabled by environment configuration."""
    return os.getenv("LANGSMITH_TRACING", "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def get_langsmith_config() -> dict[str, Any]:
    """Return non-secret LangSmith configuration for diagnostics/tests."""
    return {
        "enabled": is_langsmith_tracing_enabled(),
        "project": os.getenv("LANGSMITH_PROJECT", DEFAULT_PROJECT),
        "endpoint": os.getenv("LANGSMITH_ENDPOINT", DEFAULT_LANGSMITH_ENDPOINT),
        "has_api_key": bool(os.getenv("LANGSMITH_API_KEY", "").strip()),
    }


def build_trace_config(query: str) -> dict[str, Any]:
    """Build LangGraph run metadata without exposing secrets."""
    return {
        "run_name": "financial-analyst-agent",
        "tags": ["financial-analyst-agent"],
        "metadata": {
            "query_length": len(query),
            "langsmith_tracing_enabled": is_langsmith_tracing_enabled(),
        },
    }

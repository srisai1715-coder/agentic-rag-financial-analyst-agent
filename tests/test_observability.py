from app.observability.tracing import (
    build_trace_config,
    get_langsmith_config,
    is_langsmith_tracing_enabled,
)


def test_langsmith_tracing_disabled_by_default(monkeypatch):
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)
    assert is_langsmith_tracing_enabled() is False


def test_langsmith_config_never_returns_api_key(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "true")
    monkeypatch.setenv("LANGSMITH_API_KEY", "secret-value")
    monkeypatch.setenv("LANGSMITH_PROJECT", "test-project")

    config = get_langsmith_config()

    assert config["enabled"] is True
    assert config["project"] == "test-project"
    assert config["has_api_key"] is True
    assert "secret-value" not in str(config)


def test_trace_config_contains_safe_metadata(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "true")

    config = build_trace_config("What was Microsoft's revenue in fiscal year 2025?")

    assert config["run_name"] == "financial-analyst-agent"
    assert "financial-analyst-agent" in config["tags"]
    assert config["metadata"]["query_length"] > 0
    assert config["metadata"]["langsmith_tracing_enabled"] is True

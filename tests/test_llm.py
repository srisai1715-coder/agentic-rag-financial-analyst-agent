import pytest

from app.llm.client import GroqChatClient


def test_llm_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        GroqChatClient(api_key="")
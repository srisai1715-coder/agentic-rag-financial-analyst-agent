import pytest

from app.rag.embeddings import CohereEmbeddingClient


def test_embedding_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("COHERE_API_KEY", raising=False)
    monkeypatch.delenv("EMBEDDING_API_KEY", raising=False)
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)
    with pytest.raises(ValueError, match="COHERE_API_KEY"):
        CohereEmbeddingClient(api_key="")
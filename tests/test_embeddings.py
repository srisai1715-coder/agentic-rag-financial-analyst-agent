import pytest

from app.rag.embeddings import NVIDIAEmbeddingClient


def test_embedding_client_requires_api_key():
    with pytest.raises(ValueError, match="NVIDIA_API_KEY"):
        NVIDIAEmbeddingClient(api_key="")

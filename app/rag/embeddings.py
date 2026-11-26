import os
import cohere

from app.config import COHERE_API_KEY, COHERE_EMBEDDING_MODEL


class CohereEmbeddingClient:
    """Wrapper around Cohere's v2 Embed API."""

    def __init__(
        self,
        api_key: str = COHERE_API_KEY,
        model: str = COHERE_EMBEDDING_MODEL,
    ):
        resolved_key = api_key or os.getenv("COHERE_API_KEY", "")
        resolved_model = model or os.getenv("COHERE_EMBEDDING_MODEL", "embed-v5.0-fast")

        if not resolved_key:
            raise ValueError(
                "COHERE_API_KEY is missing. Add it to your .env file."
            )
        if not resolved_model:
            raise ValueError(
                "COHERE_EMBEDDING_MODEL is missing. Add it to your .env file."
            )

        self.client = cohere.ClientV2(api_key=resolved_key)
        self.model = resolved_model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        inputs = [
            {
                "content": [
                    {"type": "text", "text": text},
                ]
            }
            for text in texts
        ]
        response = self.client.embed(
            inputs=inputs,
            model=self.model,
            input_type="search_document",
            embedding_types=["float"],
        )
        return list(response.embeddings.float or [])

    def embed_query(self, text: str) -> list[float]:
        if not text:
            return []

        inputs = [
            {
                "content": [
                    {"type": "text", "text": text},
                ]
            }
        ]
        response = self.client.embed(
            inputs=inputs,
            model=self.model,
            input_type="search_query",
            embedding_types=["float"],
        )
        vectors = list(response.embeddings.float or [])
        return vectors[0] if vectors else []


# Backward-compatible aliases so existing imports continue working.
EmbeddingClient = CohereEmbeddingClient
NVIDIAEmbeddingClient = CohereEmbeddingClient
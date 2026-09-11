from openai import OpenAI

from app.config import (
    NVIDIA_API_BASE_URL,
    NVIDIA_API_KEY,
    NVIDIA_EMBEDDING_MODEL,
)


class NVIDIAEmbeddingClient:
    """Small wrapper around NVIDIA's OpenAI-compatible embeddings API."""

    def __init__(
        self,
        api_key: str = NVIDIA_API_KEY,
        base_url: str = NVIDIA_API_BASE_URL,
        model: str = NVIDIA_EMBEDDING_MODEL,
    ):
        if not api_key:
            raise ValueError(
                "NVIDIA_API_KEY is missing. Add it to your .env file."
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

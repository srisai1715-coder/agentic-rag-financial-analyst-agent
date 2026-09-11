from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import (
    LOCAL_QDRANT_PATH,
    QDRANT_API_KEY,
    QDRANT_COLLECTION,
    QDRANT_URL,
    QDRANT_VECTOR_SIZE,
)


def get_qdrant_client(
    local_path: str | Path = LOCAL_QDRANT_PATH,
    url: str = QDRANT_URL,
    api_key: str = QDRANT_API_KEY,
) -> QdrantClient:
    """Use Qdrant Cloud when QDRANT_URL is set; otherwise use local disk."""
    if url:
        return QdrantClient(url=url, api_key=api_key or None)

    path = Path(local_path)
    path.mkdir(parents=True, exist_ok=True)
    return QdrantClient(path=str(path))


def ensure_collection(client: QdrantClient) -> None:
    """Create the collection if it does not already exist."""
    collections = client.get_collections().collections
    names = {collection.name for collection in collections}

    if QDRANT_COLLECTION not in names:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=QDRANT_VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

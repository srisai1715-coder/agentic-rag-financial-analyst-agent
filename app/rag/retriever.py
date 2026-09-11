from app.config import QDRANT_COLLECTION
from app.database.qdrant import get_qdrant_client
from app.rag.embeddings import NVIDIAEmbeddingClient

class QdrantRetriever:
    def __init__(self):
        self.embedding_client = NVIDIAEmbeddingClient()
        self.client = get_qdrant_client()

    def search(self, query, top_k=5, min_score=None):
        if not query.strip():
            raise ValueError("query must not be empty")
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")
        vector = self.embedding_client.embed_query(query)
        results = self.client.query_points(
            collection_name=QDRANT_COLLECTION,
            query=vector,
            limit=top_k,
            with_payload=True,
        ).points
        output = []
        for result in results:
            if min_score is not None and result.score < min_score:
                continue
            output.append({
                "score": result.score,
                "chunk_id": result.payload.get("chunk_id", str(result.id)),
                "text": result.payload.get("text", ""),
                "metadata": {
                    "document": result.payload.get("document"),
                    "page": result.payload.get("page"),
                    "chunk_index": result.payload.get("chunk_index"),
                },
            })
        return output

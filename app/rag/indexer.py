import argparse
import json
import uuid
from pathlib import Path
from qdrant_client.models import PointStruct
from app.config import CHUNKS_PATH, QDRANT_COLLECTION
from app.database.qdrant import ensure_collection, get_qdrant_client
from app.rag.embeddings import NVIDIAEmbeddingClient

def load_chunks(path=CHUNKS_PATH):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Chunks file not found: {path}. Run `python -m app.rag.ingestion` first.")
    with path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]

def qdrant_point_id(chunk_id: str) -> str:
    # Qdrant local mode accepts UUID/int IDs, not readable IDs such as page-2-chunk-0.
    return str(uuid.uuid5(uuid.NAMESPACE_URL, chunk_id))

def index_chunks(chunks_path=CHUNKS_PATH, batch_size=32):
    chunks = load_chunks(chunks_path)
    if not chunks:
        raise ValueError("No chunks found to index.")
    embedding_client = NVIDIAEmbeddingClient()
    qdrant = get_qdrant_client()
    ensure_collection(qdrant)
    total = 0
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        vectors = embedding_client.embed_documents([item["text"] for item in batch])
        points = [
            PointStruct(
                id=qdrant_point_id(item["chunk_id"]),
                vector=vector,
                payload={"chunk_id": item["chunk_id"], "text": item["text"], **item["metadata"]},
            )
            for item, vector in zip(batch, vectors)
        ]
        qdrant.upsert(collection_name=QDRANT_COLLECTION, points=points)
        total += len(points)
        print(f"Indexed {total}/{len(chunks)} chunks")
    return total

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunks", default=str(CHUNKS_PATH))
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()
    print(f"Indexed {index_chunks(args.chunks, args.batch_size)} chunks into '{QDRANT_COLLECTION}'")

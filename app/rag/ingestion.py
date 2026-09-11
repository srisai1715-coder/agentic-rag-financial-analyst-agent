import json
from pathlib import Path
from app.config import CHUNK_OVERLAP, CHUNK_SIZE, CHUNKS_PATH, PDF_PATH
from app.rag.chunking import chunk_page_text
from app.rag.pdf_loader import load_pdf_pages

def build_chunks(pdf_path=PDF_PATH, output_path=CHUNKS_PATH, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    pages = load_pdf_pages(pdf_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output.open("w", encoding="utf-8") as file:
        for page in pages:
            for chunk_index, text in enumerate(chunk_page_text(page["text"], chunk_size, overlap)):
                file.write(json.dumps({
                    "chunk_id": f"page-{page['page']}-chunk-{chunk_index}",
                    "text": text,
                    "metadata": {"document": Path(pdf_path).name, "page": page["page"], "chunk_index": chunk_index}
                }, ensure_ascii=False) + "\n")
                count += 1
    return count

if __name__ == "__main__":
    print(f"Created {build_chunks()} chunks at {CHUNKS_PATH}")

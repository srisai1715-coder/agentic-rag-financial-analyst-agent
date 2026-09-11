from pathlib import Path
import pymupdf

def load_pdf_pages(pdf_path: str | Path) -> list[dict]:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    pages = []
    with pymupdf.open(path) as document:
        for page_index, page in enumerate(document):
            pages.append({"page": page_index + 1, "text": page.get_text("text") or ""})
    return pages

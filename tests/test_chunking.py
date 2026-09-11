from app.rag.chunking import chunk_page_text, normalize_text


def test_normalize_text():
    text = "Hello  world\r\n\r\n\r\nNext"
    assert normalize_text(text) == "Hello world\n\nNext"


def test_chunking_respects_size_and_overlap():
    text = " ".join(["word"] * 1000)
    chunks = chunk_page_text(text, chunk_size=100, overlap=20)

    assert chunks
    assert all(len(chunk) <= 100 for chunk in chunks)
    assert all(chunk.strip() for chunk in chunks)

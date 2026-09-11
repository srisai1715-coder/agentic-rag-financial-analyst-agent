from pathlib import Path


def format_citation(metadata: dict) -> str:
    document = metadata.get("document") or "Unknown document"
    page = metadata.get("page")

    if page is not None:
        return f"{Path(document).name}, p. {page}"

    return document
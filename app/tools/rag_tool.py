from app.rag.citation import format_citation
from app.rag.retriever import QdrantRetriever


class AnnualReportRAGTool:
    name = "annual_report_rag"

    description = (
        "Search the indexed Microsoft 2025 Annual Report and return "
        "relevant evidence with PDF page citations."
    )

    def __init__(self):
        self.retriever = QdrantRetriever()

    def run(
        self,
        query: str,
        top_k: int = 5,
        min_score: float | None = None,
    ) -> dict:

        results = self.retriever.search(
            query,
            top_k=top_k,
            min_score=min_score,
        )

        sources = []
        seen = set()

        for result in results:
            citation = format_citation(result["metadata"])

            if citation not in seen:
                sources.append(citation)
                seen.add(citation)

        return {
            "query": query,
            "results": results,
            "sources": sources,
            "result_count": len(results),
        }
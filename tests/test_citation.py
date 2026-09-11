from app.rag.citation import format_citation

def test_format_citation():
    assert format_citation({"document": "2025_AnnualReport.pdf", "page": 24}) == "2025_AnnualReport.pdf, p. 24"

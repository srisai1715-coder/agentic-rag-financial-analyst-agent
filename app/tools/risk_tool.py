from typing import Any


class RiskAnalysisTool:
    """Extract and categorize risk-related evidence from retrieved report chunks."""

    name = "risk_analysis"

    RISK_CATEGORIES = {
        "cybersecurity": (
            "cybersecurity",
            "cyber attack",
            "cyberattacks",
            "security breach",
            "ransomware",
        ),
        "competition": (
            "competition",
            "competitive",
            "competitor",
            "compete",
        ),
        "regulatory": (
            "regulatory",
            "regulation",
            "government regulation",
            "antitrust",
            "legal",
        ),
        "privacy": (
            "privacy",
            "personal data",
            "data protection",
        ),
        "macroeconomic": (
            "economic",
            "macroeconomic",
            "inflation",
            "interest rates",
            "recession",
        ),
        "supply_chain": (
            "supply chain",
            "supplier",
            "shortage",
            "component",
        ),
        "technology": (
            "technology risk",
            "technological",
            "artificial intelligence",
            "ai systems",
        ),
    }

    def _categories_for_text(self, text: str) -> list[str]:
        lowered = text.lower()

        categories = []

        for category, keywords in self.RISK_CATEGORIES.items():
            if any(keyword in lowered for keyword in keywords):
                categories.append(category)

        return categories

    def run(self, evidence: list[dict[str, Any]]) -> dict[str, Any]:
        risks: list[dict[str, Any]] = []
        category_set: set[str] = set()

        for item in evidence:
            text = item.get("text", "").strip()

            if not text:
                continue

            categories = self._categories_for_text(text)

            if not categories:
                continue

            metadata = item.get("metadata", {})

            page = metadata.get("page")

            source = (
                f"p. {page}"
                if page is not None
                else "page unavailable"
            )

            risks.append(
                {
                    "categories": categories,
                    "source": source,
                    "text": text,
                }
            )

            category_set.update(categories)

        return {
            "tool": self.name,
            "risk_count": len(risks),
            "categories": sorted(category_set),
            "risks": risks,
        }
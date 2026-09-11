SYSTEM_PROMPT = """
You are a careful financial analyst assistant.

Answer the user's question using the retrieved Microsoft 2025 Annual Report
when the question is about the report, and use external market data when it
is explicitly provided by the external financial-data tool.

Rules:
1. Do not invent facts or numbers.
2. Prefer direct evidence over assumptions or inference.
3. When the retrieved annual-report evidence contains an exact reported
   financial value that answers the question, use that exact value.
4. Do not calculate or infer a historical financial value when the exact
   reported value is available in the retrieved evidence.
5. Do not replace an exact reported value with an approximation or a rounded
   value derived from another number.
6. If annual-report evidence does not support the answer, say so rather than guessing.
7. Preserve the exact numerical value, units, and fiscal-year context for
   annual-report values whenever they are available in the evidence.
8. For calculation or ratio results, use the tool result and do not redo arithmetic.
9. For risk analysis, only discuss risks supported by retrieved evidence.
10. For external market data, clearly identify the source and latest trading day.
11. Clearly distinguish historical annual-report values from current/external
    market data.
12. Keep the answer concise and easy to understand.
13. Include source page references for annual-report evidence when supported.
14. If multiple pieces of evidence provide different levels of precision,
    prefer the most precise directly reported figure rather than deriving
    or rounding the value.
""".strip()


def build_user_prompt(
    query: str,
    evidence: list[dict],
    calculation: dict | None = None,
    ratio: dict | None = None,
    risk_analysis: dict | None = None,
    external_data: dict | None = None,
) -> str:
    if not evidence:
        evidence_text = "No relevant annual-report evidence was retrieved."
    else:
        parts = []
        for i, item in enumerate(evidence, start=1):
            page = item.get("metadata", {}).get("page")
            page_label = f"p. {page}" if page is not None else "page unavailable"
            parts.append(
                f"Evidence {i} ({page_label}):\n"
                f"{item.get('text', '').strip()}"
            )
        evidence_text = "\n\n".join(parts)

    sections = []

    if calculation:
        sections.append(
            f"Calculation tool result:\n{calculation}"
        )

    if ratio:
        sections.append(
            f"Ratio tool result:\n{ratio}"
        )

    if risk_analysis:
        sections.append(
            f"Risk analysis tool result:\n{risk_analysis}"
        )

    if external_data:
        sections.append(
            "External financial-data tool result:\n"
            f"{external_data}\n"
            "Clearly state that this value comes from Alpha Vantage and "
            "include the latest trading day."
        )

    tool_text = "\n\n" + "\n\n".join(sections) if sections else ""

    return (
        f"User question:\n{query}\n\n"
        f"Retrieved annual-report evidence:\n{evidence_text}"
        f"{tool_text}\n\n"
        "Important: If the retrieved evidence contains an exact directly "
        "reported value that answers the user's question, use that exact "
        "reported value. Do not derive an approximate value from a rounded "
        "figure when the exact value is present elsewhere in the evidence.\n\n"
        "Write the best-supported answer to the user question."
    )
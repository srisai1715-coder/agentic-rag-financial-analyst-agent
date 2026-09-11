from typing import Any


class VerificationTool:
    """Fail-closed verification of generated answers against retrieved evidence."""

    name = "verification"

    def run(self, answer: str, evidence: list[dict[str, Any]], calculation: dict[str, Any] | None = None, ratio: dict[str, Any] | None = None) -> dict[str, Any]:
        if not evidence:
            return {"tool": self.name, "status": "failed", "verified": False, "reason": "No evidence was retrieved."}
        for result_obj in (calculation, ratio):
            if not result_obj:
                continue
            if result_obj.get("status") == "insufficient_evidence":
                return {"tool": self.name, "status": "failed", "verified": False, "reason": "A deterministic tool reported insufficient evidence."}
            result = result_obj.get("result")
            if result is not None:
                rounded = f"{float(result):.2f}"
                if rounded not in answer.lower() and str(result) not in answer.lower():
                    return {"tool": self.name, "status": "failed", "verified": False, "reason": f"Calculated result {rounded} is missing from the final answer."}
        return {"tool": self.name, "status": "passed", "verified": True, "reason": "Retrieved evidence and deterministic tool results passed verification."}

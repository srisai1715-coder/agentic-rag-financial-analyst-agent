from app.tools.verification_tool import VerificationTool


def test_verification_passes_with_evidence():
    result = VerificationTool().run(
        "Microsoft reported revenue of $281.7 billion.",
        [{"text": "Revenue was $281.7 billion.", "metadata": {"page": 2}}],
    )
    assert result["verified"] is True
    assert result["status"] == "passed"


def test_verification_fails_without_evidence():
    result = VerificationTool().run("Revenue was $281.7 billion.", [])
    assert result["verified"] is False
    assert result["status"] == "failed"


def test_verification_requires_calculation_result():
    calculation = {"operation": "revenue_growth", "result": 14.93}
    passed = VerificationTool().run("Revenue increased by 14.93%.", [{"text": "Revenue increased.", "metadata": {"page": 2}}], calculation=calculation)
    failed = VerificationTool().run("Revenue increased by 15.20%.", [{"text": "Revenue increased.", "metadata": {"page": 2}}], calculation=calculation)
    assert passed["verified"] is True
    assert failed["verified"] is False


def test_verification_fails_for_insufficient_calculation_evidence():
    result = VerificationTool().run(
        "The growth could not be determined.",
        [{"text": "Revenue data is incomplete.", "metadata": {"page": 2}}],
        calculation={"status": "insufficient_evidence"},
    )
    assert result["verified"] is False

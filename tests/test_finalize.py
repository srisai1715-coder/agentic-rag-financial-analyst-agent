from app.agent.graph import finalize


def test_finalize_keeps_verified_answer():
    assert finalize({"final_answer": "Verified.", "verification": {"verified": True}}) == {}


def test_finalize_fails_closed_when_unverified():
    result = finalize({"final_answer": "Unsupported.", "verification": {"verified": False}})
    assert "could not provide a verified answer" in result["final_answer"].lower()


def test_finalize_fails_closed_when_verification_missing():
    result = finalize({"final_answer": "Potentially unsupported."})
    assert "could not provide a verified answer" in result["final_answer"].lower()

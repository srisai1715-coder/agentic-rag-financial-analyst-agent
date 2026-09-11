from app.agent.prompts import build_user_prompt

def test_prompt_contains_question_and_evidence():
    prompt = build_user_prompt(
        "What was revenue?",
        [{"text": "Revenue was $281.7 billion.", "metadata": {"page": 21}}],
    )
    assert "What was revenue?" in prompt
    assert "$281.7 billion" in prompt
    assert "p. 21" in prompt

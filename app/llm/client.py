from openai import OpenAI

from app.config import GROQ_API_BASE_URL, GROQ_API_KEY, GROQ_LLM_MODEL

try:
    from langsmith.wrappers import wrap_openai
except ImportError:  # pragma: no cover - requirements installs LangSmith in normal use
    wrap_openai = None


class GroqChatClient:
    def __init__(
        self,
        api_key: str = GROQ_API_KEY,
        base_url: str = GROQ_API_BASE_URL,
        model: str = GROQ_LLM_MODEL,
    ):
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

        client = OpenAI(api_key=api_key, base_url=base_url)
        # LangSmith's OpenAI wrapper creates an LLM trace when LANGSMITH_TRACING=true.
        # With tracing disabled it behaves like the normal OpenAI client.
        self.client = wrap_openai(client) if wrap_openai is not None else client
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            max_tokens=1200,
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("Groq LLM returned an empty response.")
        return content.strip()


# Backward-compatible alias if any module imports NVIDIAChatClient directly.
NVIDIAChatClient = GroqChatClient
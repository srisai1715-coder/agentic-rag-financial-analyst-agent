import pytest
from app.llm.client import NVIDIAChatClient

def test_llm_client_requires_api_key():
    with pytest.raises(ValueError, match="NVIDIA_API_KEY"):
        NVIDIAChatClient(api_key="")

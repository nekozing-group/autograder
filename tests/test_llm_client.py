from src.clients.llm_client import LLMClient

def test_llm_client():
    client = LLMClient()
    assert len(client.template.template) > 0
from src.clients.llm_client import PROMPT_TEMPLATE

def test_llm_client():
    assert len(PROMPT_TEMPLATE.template) > 0
import pytest

from prosodia.errors import AdapterError
from prosodia.llm.base import LLMAdapter
from prosodia.llm.openai_compat import OpenAICompatibleAdapter


def fake_chat(messages):
    # Inspect the system prompt to decide which canned reply to return.
    system = messages[0]["content"]
    if "韵律" in system:
        return '{"phrases": ["你好", "世界"], "emphasis": ["世界"]}'
    return "二零二六年"


def test_is_an_adapter():
    assert isinstance(OpenAICompatibleAdapter(chat_fn=fake_chat), LLMAdapter)


def test_normalize_uses_transport():
    adapter = OpenAICompatibleAdapter(chat_fn=fake_chat)
    assert adapter.normalize("2026年") == "二零二六年"


def test_predict_prosody_parses_json():
    adapter = OpenAICompatibleAdapter(chat_fn=fake_chat)
    pred = adapter.predict_prosody("你好，世界")
    assert pred.phrases == ["你好", "世界"]
    assert pred.emphasis == ("世界",)


def test_invalid_json_raises():
    adapter = OpenAICompatibleAdapter(chat_fn=lambda m: "not json")
    with pytest.raises(AdapterError):
        adapter.predict_prosody("你好")


def test_fenced_json_is_tolerated():
    reply = '```json\n{"phrases": ["甲", "乙"]}\n```'
    adapter = OpenAICompatibleAdapter(chat_fn=lambda m: reply)
    pred = adapter.predict_prosody("甲乙")
    assert pred.phrases == ["甲", "乙"]

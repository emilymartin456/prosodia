from prosodia.frontend.normalize.pipeline import Normalizer
from prosodia.llm.base import LLMAdapter
from prosodia.llm.rulebased import RuleBasedAdapter
from prosodia.types import Language


def test_is_an_adapter():
    assert isinstance(RuleBasedAdapter(), LLMAdapter)


def test_normalize_matches_frontend():
    text = "2026年7月5日"
    adapter = RuleBasedAdapter()
    assert adapter.normalize(text, Language.ZH) == Normalizer(Language.ZH).normalize(text)


def test_predict_prosody_splits_on_punctuation():
    pred = RuleBasedAdapter().predict_prosody("你好，世界。今天很好")
    assert pred.phrases == ["你好", "世界", "今天很好"]
    assert pred.num_phrases == 3


def test_emphasis_flags_number_phrases():
    pred = RuleBasedAdapter().predict_prosody("共有3个，好的")
    assert any("3" in e for e in pred.emphasis)


def test_empty_input():
    pred = RuleBasedAdapter().predict_prosody("   ")
    assert pred.phrases == []

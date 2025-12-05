from prosodia.llm.base import LLMAdapter, ProsodyPrediction
from prosodia.llm.cache import CachingAdapter
from prosodia.types import Language


class CountingAdapter(LLMAdapter):
    name = "counting"

    def __init__(self):
        self.calls = 0

    def normalize(self, text, language=Language.AUTO):
        self.calls += 1
        return f"norm:{text}"

    def predict_prosody(self, text, language=Language.AUTO):
        self.calls += 1
        return ProsodyPrediction(phrases=[text], emphasis=())


def test_normalize_is_cached(tmp_path):
    inner = CountingAdapter()
    adapter = CachingAdapter(inner, tmp_path)
    assert adapter.normalize("你好") == "norm:你好"
    assert adapter.normalize("你好") == "norm:你好"
    assert inner.calls == 1  # second call served from disk


def test_prosody_is_cached(tmp_path):
    inner = CountingAdapter()
    adapter = CachingAdapter(inner, tmp_path)
    first = adapter.predict_prosody("你好")
    second = adapter.predict_prosody("你好")
    assert first.phrases == second.phrases
    assert inner.calls == 1


def test_distinct_inputs_are_separate(tmp_path):
    inner = CountingAdapter()
    adapter = CachingAdapter(inner, tmp_path)
    adapter.normalize("a")
    adapter.normalize("b")
    assert inner.calls == 2


def test_cache_persists_across_instances(tmp_path):
    CachingAdapter(CountingAdapter(), tmp_path).normalize("x")
    inner = CountingAdapter()
    assert CachingAdapter(inner, tmp_path).normalize("x") == "norm:x"
    assert inner.calls == 0

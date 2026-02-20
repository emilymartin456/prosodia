"""A content-addressed on-disk cache wrapping any adapter.

Wrapping a networked adapter with :class:`CachingAdapter` makes runs reproducible
and cheap: identical inputs return the exact same normalization / prosody without
re-querying the model. Keys are a stable hash of (adapter name, method, language,
text); values are JSON files under ``cache_dir``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from prosodia.llm.base import LLMAdapter, ProsodyPrediction
from prosodia.types import Language


def _key(parts: tuple[str, ...]) -> str:
    digest = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()
    return digest[:32]


class CachingAdapter(LLMAdapter):
    """Memoize another adapter's results to ``cache_dir``."""

    def __init__(self, inner: LLMAdapter, cache_dir: str | Path) -> None:
        self.inner = inner
        self.name = f"cached:{inner.name}"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, method: str, language: Language, text: str) -> Path:
        return self.cache_dir / f"{_key((self.inner.name, method, language.value, text))}.json"

    def normalize(self, text: str, language: Language = Language.AUTO) -> str:
        path = self._path("normalize", language, text)
        if path.exists():
            return str(json.loads(path.read_text(encoding="utf-8"))["value"])
        value = self.inner.normalize(text, language)
        path.write_text(json.dumps({"value": value}, ensure_ascii=False), encoding="utf-8")
        return value

    def predict_prosody(self, text: str, language: Language = Language.AUTO) -> ProsodyPrediction:
        path = self._path("prosody", language, text)
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return ProsodyPrediction(phrases=data["phrases"], emphasis=tuple(data["emphasis"]))
        pred = self.inner.predict_prosody(text, language)
        path.write_text(
            json.dumps(
                {"phrases": pred.phrases, "emphasis": list(pred.emphasis)}, ensure_ascii=False
            ),
            encoding="utf-8",
        )
        return pred

"""The default, fully offline adapter.

It reuses the frontend's rule-based :class:`Normalizer` for text normalization
and splits on punctuation for prosodic phrasing, so the pipeline works with no
network and no model weights — the reproducible, offline-first default.
"""

from __future__ import annotations

import re

from prosodia.frontend.normalize.pipeline import Normalizer
from prosodia.llm.base import LLMAdapter, ProsodyPrediction
from prosodia.types import Language

_PHRASE_SPLIT = re.compile(r"[。！？!?;；，,、:：\n]+")
_NUMBERISH = re.compile(r"\d")


class RuleBasedAdapter(LLMAdapter):
    name = "rule"

    def normalize(self, text: str, language: Language = Language.AUTO) -> str:
        return Normalizer(language).normalize(text)

    def predict_prosody(self, text: str, language: Language = Language.AUTO) -> ProsodyPrediction:
        phrases = [p.strip() for p in _PHRASE_SPLIT.split(text) if p.strip()]
        if not phrases:
            phrases = [text.strip()] if text.strip() else []
        # Heuristic emphasis: spans that still contain digits carry information.
        emphasis = tuple(p for p in phrases if _NUMBERISH.search(p))
        return ProsodyPrediction(phrases=phrases, emphasis=emphasis)

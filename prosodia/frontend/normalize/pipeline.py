"""Compose the individual normalizers into one language-aware pass.

``Normalizer`` runs the ordered rewrite chain (dates/times, then currency /
percent / units, then any remaining bare numbers) and collapses whitespace.
"""

from __future__ import annotations

import re

from prosodia.frontend.normalize import numbers_en, numbers_zh
from prosodia.frontend.normalize.datetime import normalize_datetime
from prosodia.frontend.normalize.units import normalize_units
from prosodia.types import Language

_CJK = re.compile(r"[一-鿿]")
_NUMBER = re.compile(r"\d+(?:\.\d+)?")
_EN_MONEY = re.compile(r"\$(\d+(?:\.\d+)?)")
_EN_PERCENT = re.compile(r"(\d+(?:\.\d+)?)%")
_WS = re.compile(r"\s+")


def detect_language(text: str) -> Language:
    """Guess the dominant language: Chinese if any CJK char is present."""
    return Language.ZH if _CJK.search(text) else Language.EN


def _collapse_ws(text: str) -> str:
    return _WS.sub(" ", text).strip()


class Normalizer:
    """Rewrite written forms into their spoken reading."""

    def __init__(self, language: Language = Language.AUTO) -> None:
        self.language = language

    def normalize(self, text: str) -> str:
        lang = self.language
        if lang == Language.AUTO:
            lang = detect_language(text)
        return self._normalize_en(text) if lang == Language.EN else self._normalize_zh(text)

    def _normalize_zh(self, text: str) -> str:
        text = normalize_datetime(text)
        text = normalize_units(text)
        text = _NUMBER.sub(lambda m: numbers_zh.read_decimal(m.group(0)), text)
        return _collapse_ws(text)

    def _normalize_en(self, text: str) -> str:
        text = _EN_MONEY.sub(lambda m: numbers_en.read_decimal(m.group(1)) + " dollars", text)
        text = _EN_PERCENT.sub(lambda m: numbers_en.read_decimal(m.group(1)) + " percent", text)
        text = _NUMBER.sub(lambda m: numbers_en.read_decimal(m.group(0)), text)
        return _collapse_ws(text)

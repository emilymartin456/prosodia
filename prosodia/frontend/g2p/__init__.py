"""Grapheme-to-phoneme conversion for Chinese and (approximately) English."""

from __future__ import annotations

from prosodia.frontend.g2p.chinese import chinese_g2p, to_pinyin
from prosodia.frontend.g2p.english import english_g2p

__all__ = ["chinese_g2p", "to_pinyin", "english_g2p"]

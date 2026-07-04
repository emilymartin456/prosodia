"""Grapheme-to-phoneme conversion for Chinese and (approximately) English."""

from __future__ import annotations

from prosodia.frontend.g2p.chinese import chinese_g2p, to_pinyin

__all__ = ["chinese_g2p", "to_pinyin"]

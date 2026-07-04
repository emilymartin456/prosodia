"""Chinese grapheme-to-phoneme via :mod:`pypinyin`.

We stay a thin wrapper over pypinyin's ``TONE3`` output and only add the parts a
synthesis frontend needs: splitting each syllable into an initial/final pair of
:class:`~prosodia.types.Phone` objects and carrying the tone through.
"""

from __future__ import annotations

from pypinyin import Style, lazy_pinyin

from prosodia.frontend.symbols import split_initial_final
from prosodia.types import Phone, Syllable


def to_pinyin(text: str) -> list[str]:
    """Return TONE3 pinyin syllables, neutral tone marked as 5."""
    return lazy_pinyin(text, style=Style.TONE3, neutral_tone_with_five=True)


def pinyin_to_syllable(pinyin: str) -> Syllable:
    """Turn a single ``"zhang1"``-style token into a :class:`Syllable`."""
    tone = 0
    body = pinyin
    if body and body[-1].isdigit():
        tone = int(body[-1])
        body = body[:-1]

    initial, final = split_initial_final(body)
    phones: list[Phone] = []
    if initial:
        phones.append(Phone(initial, tone=0, is_vowel=False))
    if final:
        phones.append(Phone(final, tone=tone, is_vowel=True))
    if not phones:  # pragma: no cover - defensive, empty token
        phones.append(Phone(body or "sil", tone=tone))
    return Syllable(text=pinyin, phones=phones, tone=tone)


def chinese_g2p(text: str) -> list[Syllable]:
    """Convert a run of Chinese text to a list of syllables (no sandhi yet)."""
    return [pinyin_to_syllable(py) for py in to_pinyin(text) if py.strip()]

"""Phonetic symbol inventory and punctuation tables shared by the frontend.

The pinyin inventory follows the ``TONE3`` convention (tone as a trailing digit
1-5, 5 = neutral) that :mod:`pypinyin` produces, which keeps the g2p stage a
thin wrapper rather than a re-implementation.
"""

from __future__ import annotations

from prosodia.types import BreakLevel

# Mandarin initials (声母). "" (zero initial) is handled implicitly.
INITIALS: tuple[str, ...] = (
    "b",
    "p",
    "m",
    "f",
    "d",
    "t",
    "n",
    "l",
    "g",
    "k",
    "h",
    "j",
    "q",
    "x",
    "zh",
    "ch",
    "sh",
    "r",
    "z",
    "c",
    "s",
    "y",
    "w",
)

# Vowel letters used to locate the syllable nucleus inside a final.
VOWEL_LETTERS: frozenset[str] = frozenset("aeiouv")

# Punctuation that ends a prosodic sentence vs. a shorter phrase.
SENTENCE_PUNCT: frozenset[str] = frozenset("。！？!?;；…")
PHRASE_PUNCT: frozenset[str] = frozenset("，,、:：")

# A neutral silence token inserted at strong boundaries.
SILENCE = "sil"


def break_for_punct(ch: str) -> BreakLevel:
    """Map a punctuation character to the break strength it induces."""
    if ch in SENTENCE_PUNCT:
        return BreakLevel.SENTENCE
    if ch in PHRASE_PUNCT:
        return BreakLevel.PHRASE
    return BreakLevel.NONE


def split_initial_final(pinyin: str) -> tuple[str, str]:
    """Split a toneless pinyin syllable into (initial, final).

    ``"zhang" -> ("zh", "ang")``, ``"an" -> ("", "an")``. Two-letter initials
    are checked before single-letter ones so ``"sh"`` wins over ``"s"``.
    """
    for initial in ("zh", "ch", "sh"):
        if pinyin.startswith(initial):
            return initial, pinyin[len(initial) :]
    if pinyin and pinyin[0] in "bpmfdtnlgkhjqxrzcsyw":
        return pinyin[0], pinyin[1:]
    return "", pinyin

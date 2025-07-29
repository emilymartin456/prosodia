"""A lightweight letter-to-sound fallback for embedded Latin words.

This is intentionally approximate — no bundled pronunciation dictionary — so
that mixed-language input still produces audible output from the reference
backend. Each whitespace-separated word becomes one syllable whose phones are
its letters, with vowels flagged so the backend voices them.
"""

from __future__ import annotations

from prosodia.types import Phone, Syllable

_VOWELS = frozenset("aeiou")
# A few digraphs worth keeping together so they read as a single sound.
_DIGRAPHS = ("ch", "sh", "th", "ph", "ng", "oo", "ee", " ")


def _split_letters(word: str) -> list[str]:
    units: list[str] = []
    i = 0
    low = word.lower()
    while i < len(low):
        pair = low[i : i + 2]
        if pair in _DIGRAPHS and pair.strip():
            units.append(pair)
            i += 2
        else:
            units.append(low[i])
            i += 1
    return units


def english_word_to_syllable(word: str) -> Syllable:
    phones: list[Phone] = []
    for unit in _split_letters(word):
        is_vowel = any(c in _VOWELS for c in unit)
        phones.append(Phone(unit, tone=0, is_vowel=is_vowel))
    if not phones:
        phones.append(Phone("sil"))
    return Syllable(text=word, phones=phones, tone=0)


def english_g2p(text: str) -> list[Syllable]:
    return [english_word_to_syllable(w) for w in text.split() if w]

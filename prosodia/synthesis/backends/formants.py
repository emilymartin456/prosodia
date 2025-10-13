"""Formant frequencies for finals and articulation classes for initials.

These tables drive the reference source-filter synthesizer. The formant values
are rough textbook averages, not speaker-calibrated — enough to make vowels
sound distinct without pretending to be a trained model.
"""

from __future__ import annotations

# (F1, F2, F3) in Hz for common pinyin finals / vowel nuclei.
VOWEL_FORMANTS: dict[str, tuple[float, float, float]] = {
    "a": (800, 1200, 2900),
    "o": (500, 900, 2600),
    "e": (500, 1600, 2600),
    "i": (300, 2300, 3000),
    "u": (320, 800, 2500),
    "v": (320, 1650, 2400),
    "ai": (700, 1400, 2600),
    "ei": (450, 2000, 2700),
    "ao": (650, 1000, 2600),
    "ou": (500, 900, 2500),
    "an": (700, 1300, 2600),
    "en": (500, 1500, 2500),
    "ang": (750, 1100, 2600),
    "eng": (520, 1550, 2550),
    "in": (350, 2100, 2900),
    "ing": (350, 2200, 3000),
    "ong": (480, 900, 2500),
    "iou": (400, 1600, 2700),
    "uei": (400, 1400, 2600),
    "er": (500, 1400, 1700),
}
DEFAULT_FORMANTS: tuple[float, float, float] = (600, 1500, 2600)

# Nasal/liquid/glide murmurs use lower, softer formants.
MURMUR_FORMANTS: tuple[float, float, float] = (300, 1100, 2300)

_FRICATIVES = frozenset({"f", "s", "sh", "x", "h", "r"})
_PLOSIVES = frozenset({"b", "p", "d", "t", "g", "k"})
_AFFRICATES = frozenset({"z", "c", "zh", "ch", "j", "q"})
_NASALS = frozenset({"m", "n"})
_APPROXIMANTS = frozenset({"l", "y", "w"})


def formants_for(final: str) -> tuple[float, float, float]:
    """Look up formants for a final, falling back to its dominant vowel."""
    if final in VOWEL_FORMANTS:
        return VOWEL_FORMANTS[final]
    for candidate in (final.rstrip("ng"), final[:2], final[:1]):
        if candidate in VOWEL_FORMANTS:
            return VOWEL_FORMANTS[candidate]
    for letter in final:
        if letter in VOWEL_FORMANTS:
            return VOWEL_FORMANTS[letter]
    return DEFAULT_FORMANTS


def consonant_class(symbol: str) -> str:
    """Classify an initial into a broad manner-of-articulation bucket."""
    if symbol in _FRICATIVES:
        return "fricative"
    if symbol in _PLOSIVES:
        return "plosive"
    if symbol in _AFFRICATES:
        return "affricate"
    if symbol in _NASALS:
        return "nasal"
    if symbol in _APPROXIMANTS:
        return "approximant"
    return "other"

"""A deterministic duration model.

Durations start from per-class base values (vowels are longer than consonants),
are shortened for neutral-tone syllables, and are divided by the requested speed
so ``rate > 1`` yields shorter, faster speech. It is intentionally simple and
rule-based; a learned duration predictor can replace :func:`phone_duration`
behind the same signature.
"""

from __future__ import annotations

from prosodia.types import Phone, ProsodyTargets, Syllable

BASE_VOWEL = 0.18  # seconds
BASE_CONSONANT = 0.06
NEUTRAL_TONE_FACTOR = 0.6
MIN_DURATION = 0.02


def phone_duration(phone: Phone, targets: ProsodyTargets) -> float:
    base = BASE_VOWEL if phone.is_vowel else BASE_CONSONANT
    if phone.is_vowel and phone.tone == 5:
        base *= NEUTRAL_TONE_FACTOR
    return max(MIN_DURATION, base / targets.rate)


def syllable_duration(syllable: Syllable, targets: ProsodyTargets) -> float:
    return sum(phone_duration(p, targets) for p in syllable.phones)

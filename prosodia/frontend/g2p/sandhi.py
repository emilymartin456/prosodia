"""Mandarin tone sandhi applied to a list of syllables in place.

Two rules cover the bulk of everyday sandhi:

* **Third-tone sandhi** — in a run of tone-3 syllables every syllable except the
  last becomes tone 2 (``你好`` ``ni3 hao3`` -> ``ni2 hao3``).
* **不 / 一 sandhi** — ``不`` becomes tone 2 before a tone-4 syllable; ``一``
  becomes tone 2 before tone 4 and tone 4 before tones 1/2/3.

The 不 / 一 detection is by pinyin surface form, which is a deliberate
simplification: it can fire on rare homographs, but for running text it is right
the overwhelming majority of the time.
"""

from __future__ import annotations

from prosodia.types import Syllable


def _retone(syllable: Syllable, tone: int) -> None:
    syllable.tone = tone
    for phone in syllable.phones:
        if phone.is_vowel:
            phone.tone = tone
    base = syllable.text[:-1] if syllable.text[-1:].isdigit() else syllable.text
    syllable.text = f"{base}{tone}"


def _base(syllable: Syllable) -> str:
    return syllable.text[:-1] if syllable.text[-1:].isdigit() else syllable.text


def apply_third_tone_sandhi(syllables: list[Syllable]) -> list[Syllable]:
    n = len(syllables)
    i = 0
    while i < n:
        if syllables[i].tone == 3:
            j = i
            while j + 1 < n and syllables[j + 1].tone == 3:
                j += 1
            for k in range(i, j):  # all but the last in the run
                _retone(syllables[k], 2)
            i = j + 1
        else:
            i += 1
    return syllables


def apply_bu_yi_sandhi(syllables: list[Syllable]) -> list[Syllable]:
    for i in range(len(syllables) - 1):
        base = _base(syllables[i])
        nxt = syllables[i + 1].tone
        if base == "bu":
            _retone(syllables[i], 2 if nxt == 4 else 4)
        elif base == "yi":
            _retone(syllables[i], 2 if nxt == 4 else 4)
    return syllables


def apply_sandhi(syllables: list[Syllable]) -> list[Syllable]:
    """Run the sandhi rules in the conventional order (不/一 first, then 3-3)."""
    apply_bu_yi_sandhi(syllables)
    apply_third_tone_sandhi(syllables)
    return syllables

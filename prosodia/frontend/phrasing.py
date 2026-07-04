"""Prosodic phrasing: deciding where breaks fall between words.

The frontend seeds each word with a break derived from trailing punctuation; a
:class:`PhraseBreaker` then refines those, chiefly by inserting phrase breaks
into long stretches that carry no punctuation so the synthesized speech can
breathe.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from prosodia.types import BreakLevel, Word


@runtime_checkable
class PhraseBreaker(Protocol):
    """Assigns ``break_after`` on each word in place."""

    def assign(self, words: list[Word]) -> None: ...


class NoopPhraser:
    """Leaves punctuation-derived breaks untouched (useful as a baseline)."""

    def assign(self, words: list[Word]) -> None:  # noqa: D401 - trivial
        if words:
            last = words[-1]
            last.break_after = max(last.break_after, BreakLevel.SENTENCE)


class RuleBasedPhraser:
    """Insert phrase breaks so no unbroken run exceeds a syllable budget.

    Punctuation-derived breaks are respected; between them, a phrase break is
    inserted at the first word boundary once the running syllable count reaches
    ``max_syllables``. The final word is always promoted to at least a sentence
    break so the utterance ends cleanly.
    """

    def __init__(self, max_syllables: int = 12) -> None:
        if max_syllables < 1:
            raise ValueError("max_syllables must be >= 1")
        self.max_syllables = max_syllables

    def assign(self, words: list[Word]) -> None:
        run = 0
        for i, word in enumerate(words):
            run += max(1, len(word.syllables))
            if word.break_after != BreakLevel.NONE:
                run = 0
                continue
            if run >= self.max_syllables and i < len(words) - 1:
                word.break_after = BreakLevel.PHRASE
                run = 0
        if words:
            last = words[-1]
            last.break_after = BreakLevel(max(int(last.break_after), int(BreakLevel.SENTENCE)))

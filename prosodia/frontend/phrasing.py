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

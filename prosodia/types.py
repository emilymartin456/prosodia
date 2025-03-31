"""Core data types shared across the frontend, expressive and synthesis stages.

These are deliberately lightweight (dataclasses + enums, no numpy) so that the
text side of the pipeline can be used without pulling in the audio stack.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Language(str, Enum):
    """Supported languages. ``AUTO`` asks the frontend to guess per token."""

    ZH = "zh"
    EN = "en"
    AUTO = "auto"


class BreakLevel(int, Enum):
    """Prosodic boundary strength after a word.

    The ordering matters: a larger value is a stronger break and maps to a
    longer pause. ``pause_seconds`` gives the nominal silence inserted before
    any per-utterance ``pause_scale`` is applied.
    """

    NONE = 0
    WORD = 1
    PHRASE = 2
    SENTENCE = 3

    @property
    def pause_seconds(self) -> float:
        return {0: 0.0, 1: 0.03, 2: 0.16, 3: 0.36}[int(self)]


@dataclass
class Phone:
    """A single phone (initial, final nucleus, coda or silence marker)."""

    symbol: str
    tone: int = 0
    is_vowel: bool = False

    def __post_init__(self) -> None:
        if not 0 <= self.tone <= 5:
            raise ValueError(f"tone must be in 0..5, got {self.tone}")


@dataclass
class Syllable:
    """A syllable: a small run of phones sharing one tone."""

    text: str
    phones: list[Phone] = field(default_factory=list)
    tone: int = 0

    @property
    def nucleus(self) -> Phone | None:
        for p in self.phones:
            if p.is_vowel:
                return p
        return self.phones[-1] if self.phones else None


@dataclass
class Word:
    """A word plus the break that follows it."""

    text: str
    syllables: list[Syllable] = field(default_factory=list)
    break_after: BreakLevel = BreakLevel.NONE

    @property
    def phones(self) -> list[Phone]:
        return [p for syl in self.syllables for p in syl.phones]


@dataclass
class Utterance:
    """The fully analysed text: normalized string plus a word/syllable tree."""

    text: str
    normalized: str
    language: Language
    words: list[Word] = field(default_factory=list)

    def phones(self) -> list[Phone]:
        return [p for w in self.words for p in w.phones]

    def syllables(self) -> list[Syllable]:
        return [s for w in self.words for s in w.syllables]

    @property
    def num_syllables(self) -> int:
        return sum(len(w.syllables) for w in self.words)


@dataclass
class ProsodyTargets:
    """Numeric controls the synthesis stage honours.

    ``rate`` is a speed factor (``>1`` faster, so shorter durations). ``pitch_shift``
    is in semitones relative to ``base_f0``; ``pitch_range`` scales the size of the
    intonation excursion; ``energy`` scales amplitude; ``pause_scale`` stretches or
    shrinks every inter-word pause.
    """

    rate: float = 1.0
    pitch_shift: float = 0.0
    pitch_range: float = 1.0
    energy: float = 1.0
    pause_scale: float = 1.0
    base_f0: float = 200.0

    def clamped(self) -> ProsodyTargets:
        """Return a copy with each field clamped to a sane synthesis range."""

        def c(x: float, lo: float, hi: float) -> float:
            return max(lo, min(hi, x))

        return ProsodyTargets(
            rate=c(self.rate, 0.3, 3.0),
            pitch_shift=c(self.pitch_shift, -12.0, 12.0),
            pitch_range=c(self.pitch_range, 0.1, 3.0),
            energy=c(self.energy, 0.1, 3.0),
            pause_scale=c(self.pause_scale, 0.0, 4.0),
            base_f0=c(self.base_f0, 60.0, 500.0),
        )

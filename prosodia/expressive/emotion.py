"""The emotion catalogue.

Each :class:`Emotion` stores the prosodic deltas it applies at full intensity,
expressed relative to neutral speech: a pitch shift in semitones, and
multipliers for pitch range, speaking rate and energy. Chinese and English
aliases resolve to the same entry so callers can say ``"高兴"`` or ``"happy"``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from prosodia.errors import ProsodiaError


@dataclass(frozen=True)
class Emotion:
    name: str
    pitch_shift: float  # semitones relative to base
    pitch_range: float  # multiplier on intonation excursion
    rate: float  # speaking-rate multiplier
    energy: float  # amplitude multiplier
    aliases: tuple[str, ...] = field(default_factory=tuple)


_CATALOG: tuple[Emotion, ...] = (
    Emotion("neutral", 0.0, 1.0, 1.0, 1.0, ("中性", "default", "平淡")),
    Emotion("happy", 2.0, 1.30, 1.10, 1.15, ("高兴", "开心", "喜悦")),
    Emotion("sad", -2.0, 0.70, 0.90, 0.85, ("悲伤", "难过", "伤心")),
    Emotion("angry", 1.0, 1.40, 1.15, 1.30, ("愤怒", "生气")),
    Emotion("excited", 3.0, 1.50, 1.20, 1.25, ("兴奋", "激动")),
    Emotion("calm", -1.0, 0.85, 0.95, 0.95, ("平静", "冷静")),
    Emotion("serious", -1.0, 0.90, 0.95, 1.05, ("严肃", "正式")),
    Emotion("gentle", 0.0, 0.90, 0.95, 0.90, ("温柔", "轻柔")),
)

_BY_NAME: dict[str, Emotion] = {}
for _emo in _CATALOG:
    _BY_NAME[_emo.name] = _emo
    for _alias in _emo.aliases:
        _BY_NAME[_alias] = _emo


def get_emotion(name: str) -> Emotion:
    """Resolve an emotion by canonical name or alias (case-insensitive)."""
    key = name.strip().lower()
    if key in _BY_NAME:
        return _BY_NAME[key]
    if name in _BY_NAME:  # Chinese aliases are not lowercased meaningfully
        return _BY_NAME[name]
    raise ProsodiaError(f"unknown emotion: {name!r}; try one of {list_emotions()}")


def list_emotions() -> list[str]:
    """Return the canonical emotion names in catalogue order."""
    return [e.name for e in _CATALOG]

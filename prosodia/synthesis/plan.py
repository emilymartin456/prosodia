"""Assemble an utterance + style into a flat, renderable plan.

A :class:`SynthesisPlan` is a list of :class:`Segment` objects — one per phone,
plus explicit silence segments at word breaks — each carrying its duration and,
for voiced phones, an F0 track. Backends consume this and never touch the
frontend types directly.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from prosodia.expressive.style import StyleControl
from prosodia.synthesis.duration import phone_duration
from prosodia.synthesis.f0 import f0_for_tone
from prosodia.types import ProsodyTargets, Utterance

DEFAULT_F0_FPS = 200


@dataclass
class Segment:
    symbol: str
    duration: float
    is_vowel: bool
    tone: int
    energy: float
    f0: np.ndarray | None = None
    is_silence: bool = False


@dataclass
class SynthesisPlan:
    segments: list[Segment]
    sample_rate: int
    targets: ProsodyTargets
    f0_fps: int = DEFAULT_F0_FPS

    @property
    def total_duration(self) -> float:
        return sum(s.duration for s in self.segments)

    @property
    def num_voiced(self) -> int:
        return sum(1 for s in self.segments if s.is_vowel)


def build_plan(
    utterance: Utterance,
    style: StyleControl | None = None,
    sample_rate: int = 22050,
    f0_fps: int = DEFAULT_F0_FPS,
) -> SynthesisPlan:
    style = style or StyleControl()
    targets = style.to_targets()
    segments: list[Segment] = []

    for word in utterance.words:
        for syllable in word.syllables:
            for phone in syllable.phones:
                duration = phone_duration(phone, targets)
                f0 = None
                if phone.is_vowel:
                    n_frames = max(1, round(duration * f0_fps))
                    tone = phone.tone or syllable.tone
                    f0 = f0_for_tone(
                        tone,
                        n_frames,
                        base_f0=targets.base_f0,
                        pitch_shift=targets.pitch_shift,
                        pitch_range=targets.pitch_range,
                    )
                segments.append(
                    Segment(
                        symbol=phone.symbol,
                        duration=duration,
                        is_vowel=phone.is_vowel,
                        tone=phone.tone,
                        energy=targets.energy,
                        f0=f0,
                    )
                )
        pause = word.break_after.pause_seconds * targets.pause_scale
        if pause > 0:
            segments.append(
                Segment("sil", pause, is_vowel=False, tone=0, energy=0.0, is_silence=True)
            )

    return SynthesisPlan(segments, sample_rate, targets, f0_fps)

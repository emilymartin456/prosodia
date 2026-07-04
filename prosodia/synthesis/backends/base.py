"""The acoustic backend interface.

A backend only has to implement :meth:`AcousticBackend.render_segment`; the base
class assembles whole-utterance rendering and a default per-segment streaming
generator on top of it.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

import numpy as np

from prosodia.audio.chunk import AudioChunk
from prosodia.synthesis.plan import Segment, SynthesisPlan


class AcousticBackend(ABC):
    """Render a :class:`SynthesisPlan` to audio."""

    name: str = "base"

    @abstractmethod
    def render_segment(self, segment: Segment, sample_rate: int) -> np.ndarray:
        """Return float32 samples for a single segment."""

    def render(self, plan: SynthesisPlan) -> AudioChunk:
        parts = [self.render_segment(s, plan.sample_rate) for s in plan.segments]
        if parts:
            samples = np.concatenate(parts).astype(np.float32)
        else:
            samples = np.zeros(0, dtype=np.float32)
        return AudioChunk(samples, plan.sample_rate)

    def render_stream(self, plan: SynthesisPlan) -> Iterator[AudioChunk]:
        """Yield one :class:`AudioChunk` per segment, in order."""
        for segment in plan.segments:
            yield AudioChunk(self.render_segment(segment, plan.sample_rate), plan.sample_rate)

"""Real-time streaming metrics.

Pure arithmetic so it can be unit-tested without a clock. The key figure is the
real-time factor (RTF) — wall time divided by produced audio time — where values
below 1.0 mean synthesis keeps ahead of playback.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


def real_time_factor(audio_seconds: float, wall_seconds: float) -> float:
    if audio_seconds <= 0:
        return math.inf
    return wall_seconds / audio_seconds


@dataclass
class StreamStats:
    audio_seconds: float
    wall_seconds: float
    first_chunk_seconds: float | None = None
    chunks: int = 0

    @property
    def rtf(self) -> float:
        return real_time_factor(self.audio_seconds, self.wall_seconds)

    @property
    def is_realtime(self) -> bool:
        return self.rtf <= 1.0

    @property
    def throughput(self) -> float:
        """Seconds of audio produced per second of wall time."""
        if self.wall_seconds <= 0:
            return math.inf
        return self.audio_seconds / self.wall_seconds

    def summary(self) -> str:
        first = "-" if self.first_chunk_seconds is None else f"{self.first_chunk_seconds:.3f}s"
        return (
            f"{self.chunks} chunks, audio={self.audio_seconds:.2f}s, "
            f"wall={self.wall_seconds:.2f}s, RTF={self.rtf:.3f}, first_audio={first}"
        )

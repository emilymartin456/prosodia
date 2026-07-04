"""A mono, floating-point audio buffer with a sample rate attached.

Keeping samples as ``float32`` in ``[-1, 1]`` throughout the pipeline avoids the
lossy int/float juggling that creeps in when every stage picks its own format.
Conversion to 16-bit PCM only happens at the WAV boundary.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class AudioChunk:
    """One contiguous block of mono audio."""

    samples: np.ndarray  # float32, shape (n,)
    sample_rate: int

    def __post_init__(self) -> None:
        arr = np.asarray(self.samples, dtype=np.float32).reshape(-1)
        self.samples = arr
        if self.sample_rate <= 0:
            raise ValueError("sample_rate must be positive")

    def __len__(self) -> int:
        return int(self.samples.shape[0])

    @property
    def duration(self) -> float:
        """Length in seconds."""
        return len(self) / self.sample_rate

    @property
    def peak(self) -> float:
        return float(np.max(np.abs(self.samples))) if len(self) else 0.0

    def is_silent(self, threshold: float = 1e-4) -> bool:
        return self.peak < threshold

    @classmethod
    def silence(cls, seconds: float, sample_rate: int) -> AudioChunk:
        n = max(0, round(seconds * sample_rate))
        return cls(np.zeros(n, dtype=np.float32), sample_rate)

    def append(self, other: AudioChunk) -> AudioChunk:
        if other.sample_rate != self.sample_rate:
            raise ValueError(
                f"sample rate mismatch: {self.sample_rate} vs {other.sample_rate}"
            )
        return AudioChunk(
            np.concatenate([self.samples, other.samples]), self.sample_rate
        )

    def normalized(self, target_peak: float = 0.95) -> AudioChunk:
        """Scale so the loudest sample sits at ``target_peak`` (no-op if silent)."""
        p = self.peak
        if p < 1e-9:
            return self
        return AudioChunk(self.samples * (target_peak / p), self.sample_rate)


def concat(chunks: list[AudioChunk]) -> AudioChunk:
    """Join chunks that share a sample rate into one buffer."""
    if not chunks:
        raise ValueError("cannot concatenate an empty list of chunks")
    sr = chunks[0].sample_rate
    for c in chunks:
        if c.sample_rate != sr:
            raise ValueError("all chunks must share a sample rate")
    return AudioChunk(np.concatenate([c.samples for c in chunks]), sr)

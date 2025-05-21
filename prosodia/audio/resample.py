"""Sample-rate conversion helpers."""

from __future__ import annotations

import numpy as np

from prosodia.audio.chunk import AudioChunk


def resample(chunk: AudioChunk, target_rate: int) -> AudioChunk:
    """Resample ``chunk`` to ``target_rate`` with linear interpolation.

    Linear interpolation is cheap and good enough for the reference backend and
    for lining up chunks before concatenation; a polyphase resampler can be
    dropped in behind this signature later without touching callers.
    """
    if target_rate <= 0:
        raise ValueError("target_rate must be positive")
    if target_rate == chunk.sample_rate or len(chunk) == 0:
        return AudioChunk(chunk.samples.copy(), target_rate)

    n_out = max(1, round(len(chunk) * target_rate / chunk.sample_rate))
    # Sample positions in the source timeline, endpoint-inclusive.
    src_idx: np.ndarray = np.linspace(0.0, len(chunk) - 1, num=n_out, dtype=np.float64)
    grid: np.ndarray = np.arange(len(chunk), dtype=np.float64)
    out = np.interp(src_idx, grid, chunk.samples).astype(np.float32)
    return AudioChunk(out, target_rate)

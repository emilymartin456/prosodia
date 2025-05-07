"""Sample-rate conversion helpers."""

from __future__ import annotations

from prosodia.audio.chunk import AudioChunk


def resample(chunk: AudioChunk, target_rate: int) -> AudioChunk:
    """Resample ``chunk`` to ``target_rate``."""
    raise NotImplementedError

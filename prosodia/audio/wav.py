"""Read and write 16-bit PCM mono WAV files with the stdlib ``wave`` module."""

from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

from prosodia.audio.chunk import AudioChunk

_INT16_MAX = 32767


def write_wav(path: str | Path, chunk: AudioChunk) -> None:
    """Write ``chunk`` as a 16-bit PCM WAV file."""
    clipped = np.clip(chunk.samples, -1.0, 1.0)
    pcm = np.round(clipped * _INT16_MAX).astype("<i2")
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(chunk.sample_rate)
        wav.writeframes(pcm.tobytes())


def read_wav(path: str | Path) -> AudioChunk:
    """Read a mono WAV file into an :class:`AudioChunk`."""
    raise NotImplementedError

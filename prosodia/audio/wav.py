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
    with wave.open(str(path), "rb") as wav:
        n_channels = wav.getnchannels()
        width = wav.getsampwidth()
        rate = wav.getframerate()
        raw = wav.readframes(wav.getnframes())
    if width != 2:
        raise ValueError(f"only 16-bit PCM is supported, got {width * 8}-bit")
    data = np.frombuffer(raw, dtype="<i2").astype(np.float32) / _INT16_MAX
    if n_channels > 1:
        # Downmix to mono by averaging interleaved channels.
        data = data.reshape(-1, n_channels).mean(axis=1)
    return AudioChunk(data, rate)

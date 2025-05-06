"""Read and write 16-bit PCM mono WAV files with the stdlib ``wave`` module."""

from __future__ import annotations

from pathlib import Path

from prosodia.audio.chunk import AudioChunk


def write_wav(path: str | Path, chunk: AudioChunk) -> None:
    """Write ``chunk`` as a 16-bit PCM WAV file."""
    raise NotImplementedError


def read_wav(path: str | Path) -> AudioChunk:
    """Read a mono WAV file into an :class:`AudioChunk`."""
    raise NotImplementedError

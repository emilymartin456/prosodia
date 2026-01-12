"""Sinks that consume a stream of :class:`AudioChunk` objects.

A :class:`WavSink` buffers chunks and writes a single WAV on close (usable as a
context manager); a :class:`CallbackSink` forwards each chunk to a callable — the
seam where a real-time audio device or WebSocket would plug in.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from pathlib import Path
from types import TracebackType

import numpy as np

from prosodia.audio.chunk import AudioChunk, concat
from prosodia.audio.wav import write_wav


def drain(chunks: Iterable[AudioChunk], sample_rate: int = 22050) -> AudioChunk:
    """Collect a chunk stream into one :class:`AudioChunk`."""
    collected = list(chunks)
    if not collected:
        return AudioChunk(np.zeros(0, dtype=np.float32), sample_rate)
    return concat(collected)


class WavSink:
    """Accumulate chunks and write them to a WAV file on close."""

    def __init__(self, path: str | Path, sample_rate: int = 22050) -> None:
        self.path = Path(path)
        self.sample_rate = sample_rate
        self._buffers: list[AudioChunk] = []

    def write(self, chunk: AudioChunk) -> None:
        if chunk.sample_rate != self.sample_rate:
            raise ValueError("chunk sample rate does not match sink")
        self._buffers.append(chunk)

    @property
    def duration(self) -> float:
        return sum(c.duration for c in self._buffers)

    def close(self) -> AudioChunk:
        audio = drain(self._buffers, self.sample_rate)
        write_wav(self.path, audio)
        return audio

    def __enter__(self) -> WavSink:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if exc is None:
            self.close()


class CallbackSink:
    """Forward each chunk to ``callback`` as it arrives."""

    def __init__(self, callback: Callable[[AudioChunk], None]) -> None:
        self.callback = callback

    def write(self, chunk: AudioChunk) -> None:
        self.callback(chunk)

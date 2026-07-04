"""The streaming synthesis engine.

Given a frontend and a backend, :meth:`StreamingEngine.stream` chunks the input
and yields audio for each chunk as soon as it is rendered — the basis for
low-latency, real-time playback. Wall-clock timing goes through an injectable
``clock`` so behaviour is deterministic under test.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterator

import numpy as np

from prosodia.audio.chunk import AudioChunk, concat
from prosodia.expressive.style import StyleControl
from prosodia.frontend import TextFrontend
from prosodia.streaming.chunker import chunk_text
from prosodia.streaming.metrics import StreamStats
from prosodia.synthesis.backends import get_backend
from prosodia.synthesis.backends.base import AcousticBackend
from prosodia.synthesis.plan import build_plan


class StreamingEngine:
    def __init__(
        self,
        frontend: TextFrontend | None = None,
        backend: AcousticBackend | None = None,
        style: StyleControl | None = None,
        sample_rate: int = 22050,
        max_chunk_chars: int = 60,
        clock: Callable[[], float] = time.perf_counter,
    ) -> None:
        self.frontend = frontend or TextFrontend()
        self.backend = backend or get_backend("reference")
        self.style = style or StyleControl()
        self.sample_rate = sample_rate
        self.max_chunk_chars = max_chunk_chars
        self.clock = clock
        self.last_stats: StreamStats | None = None

    def stream(self, text: str) -> Iterator[AudioChunk]:
        """Yield one audio chunk per text chunk, recording stats when done."""
        start = self.clock()
        first_chunk: float | None = None
        audio_seconds = 0.0
        count = 0
        for piece in chunk_text(text, self.max_chunk_chars):
            utterance = self.frontend.process(piece)
            plan = build_plan(utterance, self.style, self.sample_rate)
            chunk = self.backend.render(plan)
            if first_chunk is None:
                first_chunk = self.clock() - start
            audio_seconds += chunk.duration
            count += 1
            yield chunk
        self.last_stats = StreamStats(
            audio_seconds=audio_seconds,
            wall_seconds=self.clock() - start,
            first_chunk_seconds=first_chunk,
            chunks=count,
        )

    def run(self, text: str) -> tuple[AudioChunk, StreamStats]:
        """Consume the whole stream and return the joined audio plus stats."""
        chunks = list(self.stream(text))
        if chunks:
            audio = concat(chunks)
        else:
            audio = AudioChunk(np.zeros(0, dtype=np.float32), self.sample_rate)
        assert self.last_stats is not None
        return audio, self.last_stats

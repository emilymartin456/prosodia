import numpy as np

from prosodia.audio.chunk import AudioChunk
from prosodia.streaming.engine import StreamingEngine
from prosodia.synthesis.backends.base import AcousticBackend


class TickClock:
    """Deterministic clock that advances one unit per call."""

    def __init__(self):
        self.t = 0.0

    def __call__(self):
        self.t += 1.0
        return self.t


class OneSampleBackend(AcousticBackend):
    name = "one"

    def render_segment(self, segment, sample_rate):
        n = max(1, round(segment.duration * sample_rate))
        return np.full(n, 0.1, dtype=np.float32)


def test_stream_yields_a_chunk_per_sentence():
    engine = StreamingEngine(backend=OneSampleBackend(), clock=TickClock())
    chunks = list(engine.stream("你好。世界。"))
    assert len(chunks) == 2
    assert all(isinstance(c, AudioChunk) for c in chunks)


def test_run_concatenates_and_reports_stats():
    engine = StreamingEngine(backend=OneSampleBackend(), clock=TickClock())
    audio, stats = engine.run("你好。世界。")
    assert len(audio) > 0
    assert stats.chunks == 2
    assert stats.first_chunk_seconds is not None
    assert stats.audio_seconds > 0


def test_empty_text_produces_empty_audio():
    engine = StreamingEngine(backend=OneSampleBackend(), clock=TickClock())
    audio, stats = engine.run("   ")
    assert len(audio) == 0
    assert stats.chunks == 0


def test_stream_is_lazy_first_chunk_latency():
    # With the tick clock, the first chunk latency is measured before the last.
    engine = StreamingEngine(backend=OneSampleBackend(), clock=TickClock())
    _, stats = engine.run("你好。世界。今天。")
    assert stats.first_chunk_seconds < stats.wall_seconds

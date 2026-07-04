import math

from prosodia.streaming.metrics import StreamStats, real_time_factor


def test_rtf_basic():
    assert real_time_factor(2.0, 1.0) == 0.5
    assert real_time_factor(1.0, 2.0) == 2.0


def test_rtf_zero_audio_is_inf():
    assert real_time_factor(0.0, 1.0) == math.inf


def test_is_realtime():
    fast = StreamStats(audio_seconds=4.0, wall_seconds=1.0)
    slow = StreamStats(audio_seconds=1.0, wall_seconds=4.0)
    assert fast.is_realtime
    assert not slow.is_realtime


def test_throughput():
    stats = StreamStats(audio_seconds=6.0, wall_seconds=2.0)
    assert stats.throughput == 3.0


def test_summary_contains_rtf():
    stats = StreamStats(audio_seconds=2.0, wall_seconds=1.0, first_chunk_seconds=0.1, chunks=3)
    text = stats.summary()
    assert "RTF" in text
    assert "3 chunks" in text

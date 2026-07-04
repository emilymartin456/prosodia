import numpy as np
import pytest

from prosodia.audio.chunk import AudioChunk, concat


def test_length_and_duration():
    c = AudioChunk(np.zeros(22050), 22050)
    assert len(c) == 22050
    assert c.duration == pytest.approx(1.0)


def test_silence_factory():
    c = AudioChunk.silence(0.5, 16000)
    assert len(c) == 8000
    assert c.is_silent()


def test_append_and_concat():
    a = AudioChunk(np.ones(10), 8000)
    b = AudioChunk(np.ones(5), 8000)
    assert len(a.append(b)) == 15
    assert len(concat([a, b, a])) == 25


def test_append_rejects_rate_mismatch():
    a = AudioChunk(np.ones(10), 8000)
    b = AudioChunk(np.ones(10), 16000)
    with pytest.raises(ValueError):
        a.append(b)


def test_normalized_hits_target_peak():
    c = AudioChunk(np.array([0.1, -0.2, 0.05]), 8000).normalized(0.9)
    assert c.peak == pytest.approx(0.9, rel=1e-5)


def test_dtype_is_float32():
    c = AudioChunk([1, 2, 3], 8000)
    assert c.samples.dtype == np.float32

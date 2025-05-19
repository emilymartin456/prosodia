import numpy as np

from prosodia.audio.chunk import AudioChunk
from prosodia.audio.resample import resample


def test_upsample_doubles_length():
    c = AudioChunk(np.ones(100), 8000)
    out = resample(c, 16000)
    assert out.sample_rate == 16000
    assert abs(len(out) - 200) <= 1


def test_downsample_halves_length():
    c = AudioChunk(np.ones(100), 16000)
    out = resample(c, 8000)
    assert abs(len(out) - 50) <= 1


def test_noop_when_rate_matches():
    c = AudioChunk(np.arange(10, dtype=np.float32), 8000)
    out = resample(c, 8000)
    assert np.array_equal(out.samples, c.samples)


def test_preserves_a_constant_signal():
    c = AudioChunk(np.full(64, 0.3, dtype=np.float32), 8000)
    out = resample(c, 22050)
    assert np.allclose(out.samples, 0.3, atol=1e-6)

import numpy as np

from prosodia.audio.chunk import AudioChunk
from prosodia.audio.wav import read_wav, write_wav


def test_wav_roundtrip(tmp_path):
    sr = 16000
    t = np.linspace(0, 0.25, int(sr * 0.25), endpoint=False)
    tone = 0.5 * np.sin(2 * np.pi * 220 * t)
    chunk = AudioChunk(tone, sr)

    path = tmp_path / "tone.wav"
    write_wav(path, chunk)
    back = read_wav(path)

    assert back.sample_rate == sr
    assert len(back) == len(chunk)
    # 16-bit quantisation error stays small.
    assert np.max(np.abs(back.samples - chunk.samples)) < 1e-3


def test_write_clips_out_of_range(tmp_path):
    chunk = AudioChunk(np.array([2.0, -3.0, 0.0]), 8000)
    path = tmp_path / "clip.wav"
    write_wav(path, chunk)
    back = read_wav(path)
    assert back.peak <= 1.0

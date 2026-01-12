import numpy as np

from prosodia.audio.chunk import AudioChunk
from prosodia.audio.wav import read_wav
from prosodia.streaming.sink import CallbackSink, WavSink, drain


def _chunk(n, sr=22050):
    return AudioChunk(np.full(n, 0.2, dtype=np.float32), sr)


def test_drain_concatenates():
    out = drain([_chunk(10), _chunk(5)])
    assert len(out) == 15


def test_drain_empty():
    out = drain([], 16000)
    assert len(out) == 0
    assert out.sample_rate == 16000


def test_wav_sink_writes_file(tmp_path):
    path = tmp_path / "out.wav"
    with WavSink(path, 22050) as sink:
        sink.write(_chunk(100))
        sink.write(_chunk(50))
    back = read_wav(path)
    assert len(back) == 150


def test_wav_sink_rejects_rate_mismatch(tmp_path):
    sink = WavSink(tmp_path / "x.wav", 22050)
    try:
        sink.write(_chunk(10, sr=16000))
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")


def test_callback_sink_forwards():
    seen = []
    sink = CallbackSink(seen.append)
    sink.write(_chunk(3))
    sink.write(_chunk(4))
    assert [len(c) for c in seen] == [3, 4]

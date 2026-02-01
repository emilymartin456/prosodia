from prosodia import ExpressiveTTS
from prosodia.audio.chunk import AudioChunk
from prosodia.audio.wav import read_wav


def test_stream_yields_audio_chunks():
    tts = ExpressiveTTS()
    chunks = list(tts.stream("你好。世界。今天天气不错。"))
    assert len(chunks) >= 2
    assert all(isinstance(c, AudioChunk) for c in chunks)
    assert all(not c.is_silent() for c in chunks)


def test_stream_to_wav_writes_and_reports_stats(tmp_path):
    tts = ExpressiveTTS()
    path = tmp_path / "story.wav"
    stats = tts.stream_to_wav("你好。世界。", path, emotion="gentle")
    assert read_wav(path).duration > 0
    assert stats.chunks == 2
    assert stats.audio_seconds > 0
    assert stats.rtf >= 0


def test_stream_respects_emotion_override():
    tts = ExpressiveTTS()
    total = sum(c.duration for c in tts.stream("你好世界。", rate=1.5))
    assert total > 0

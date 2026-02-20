import prosodia
from prosodia import ExpressiveTTS
from prosodia.expressive.style import StyleControl


def test_top_level_exports():
    assert prosodia.ExpressiveTTS is ExpressiveTTS
    assert isinstance(prosodia.__version__, str)


def test_say_produces_non_silent_audio():
    tts = ExpressiveTTS()
    chunk = tts.say("你好，世界。")
    assert not chunk.is_silent()
    assert chunk.sample_rate == 22050


def test_emotion_changes_output():
    tts = ExpressiveTTS()
    neutral = tts.say("你好世界", emotion="neutral")
    happy = tts.say("你好世界", emotion="happy")
    # Different prosody -> different waveform length or samples.
    assert neutral.samples.shape != happy.samples.shape or (neutral.samples != happy.samples).any()


def test_style_override_rate_changes_duration():
    tts = ExpressiveTTS()
    slow = tts.say("你好世界今天天气不错", rate=0.7)
    fast = tts.say("你好世界今天天气不错", rate=1.6)
    assert fast.duration < slow.duration


def test_to_wav_writes_file(tmp_path):
    from prosodia.audio.wav import read_wav

    tts = ExpressiveTTS()
    path = tmp_path / "hello.wav"
    tts.to_wav("你好", path, emotion="happy")
    assert read_wav(path).duration > 0


def test_say_with_style_control():
    tts = ExpressiveTTS()
    chunk = tts.say("你好", style=StyleControl(emotion="sad", intensity=1.0))
    assert not chunk.is_silent()

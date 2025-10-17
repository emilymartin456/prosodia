import numpy as np

from prosodia.frontend import TextFrontend
from prosodia.synthesis.backends.reference import FormantSynthBackend
from prosodia.synthesis.plan import build_plan


def _render(text):
    utt = TextFrontend().process(text)
    plan = build_plan(utt)
    return FormantSynthBackend().render(plan), plan


def test_renders_non_silent_audio():
    chunk, plan = _render("你好，世界。")
    assert chunk.sample_rate == plan.sample_rate
    assert not chunk.is_silent()
    assert chunk.peak <= 1.0


def test_duration_matches_plan():
    chunk, plan = _render("你好世界")
    assert abs(chunk.duration - plan.total_duration) < 0.05


def test_is_deterministic():
    a, _ = _render("测试一下")
    b, _ = _render("测试一下")
    assert np.array_equal(a.samples, b.samples)


def test_higher_energy_is_louder():
    from prosodia.expressive.style import StyleControl

    utt = TextFrontend().process("你好")
    quiet = FormantSynthBackend().render(build_plan(utt, StyleControl(energy=0.5)))
    loud = FormantSynthBackend().render(build_plan(utt, StyleControl(energy=1.5)))
    assert loud.peak > quiet.peak


def test_render_stream_matches_render_length():
    utt = TextFrontend().process("你好")
    plan = build_plan(utt)
    backend = FormantSynthBackend()
    streamed = sum(len(c) for c in backend.render_stream(plan))
    whole = len(backend.render(plan))
    assert streamed == whole

from prosodia.expressive.style import StyleControl
from prosodia.frontend import TextFrontend
from prosodia.synthesis.plan import build_plan


def test_plan_has_segments_and_duration():
    utt = TextFrontend().process("你好，世界。")
    plan = build_plan(utt)
    assert len(plan.segments) > 0
    assert plan.total_duration > 0.0
    assert plan.sample_rate == 22050


def test_plan_inserts_silence_at_breaks():
    utt = TextFrontend().process("你好，世界。")
    plan = build_plan(utt)
    assert any(s.is_silence for s in plan.segments)


def test_voiced_segments_carry_f0():
    utt = TextFrontend().process("你好")
    plan = build_plan(utt)
    voiced = [s for s in plan.segments if s.is_vowel]
    assert voiced
    for seg in voiced:
        assert seg.f0 is not None
        assert seg.f0.shape[0] >= 1


def test_faster_rate_shortens_plan():
    utt = TextFrontend().process("你好世界")
    slow = build_plan(utt, StyleControl(rate=0.7))
    fast = build_plan(utt, StyleControl(rate=1.6))
    assert fast.total_duration < slow.total_duration


def test_num_voiced_counts_vowels():
    utt = TextFrontend().process("你好")
    plan = build_plan(utt)
    assert plan.num_voiced == 2

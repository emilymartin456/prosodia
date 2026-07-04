from prosodia.expressive.style import StyleControl


def test_neutral_is_identity():
    t = StyleControl(emotion="neutral").to_targets()
    assert t.pitch_shift == 0.0
    assert t.rate == 1.0
    assert t.energy == 1.0


def test_happy_raises_pitch_and_energy():
    t = StyleControl(emotion="happy", intensity=1.0).to_targets()
    assert t.pitch_shift > 0.0
    assert t.energy > 1.0
    assert t.rate > 1.0


def test_zero_intensity_collapses_to_neutral():
    t = StyleControl(emotion="excited", intensity=0.0).to_targets()
    assert t.pitch_shift == 0.0
    assert t.rate == 1.0


def test_manual_override_multiplies_rate():
    base = StyleControl(emotion="neutral").to_targets()
    faster = StyleControl(emotion="neutral", rate=1.5).to_targets()
    assert faster.rate > base.rate


def test_intensity_scales_delta():
    half = StyleControl(emotion="happy", intensity=0.5).to_targets()
    full = StyleControl(emotion="happy", intensity=1.0).to_targets()
    assert half.pitch_shift < full.pitch_shift


def test_targets_are_clamped():
    t = StyleControl(emotion="excited", intensity=3.0, pitch_shift=20.0).to_targets()
    assert t.pitch_shift <= 12.0

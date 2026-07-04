from prosodia.expressive.style import StyleVector


def test_blend_endpoints():
    a = StyleVector(rate=1.0, energy=1.0)
    b = StyleVector(rate=2.0, energy=0.5)
    assert a.blend(b, 0.0) == a
    assert a.blend(b, 1.0) == b


def test_blend_midpoint():
    a = StyleVector(pitch_shift=0.0)
    b = StyleVector(pitch_shift=4.0)
    assert a.blend(b, 0.5).pitch_shift == 2.0


def test_blend_clamps_weight():
    a = StyleVector(rate=1.0)
    b = StyleVector(rate=2.0)
    assert a.blend(b, 5.0) == b
    assert a.blend(b, -1.0) == a


def test_combine_multiplies_and_adds():
    a = StyleVector(rate=1.1, pitch_shift=2.0, energy=1.2)
    b = StyleVector(rate=0.5, pitch_shift=1.0, energy=2.0)
    c = a.combine(b)
    assert c.rate == 0.55
    assert c.pitch_shift == 3.0
    assert c.energy == 2.4

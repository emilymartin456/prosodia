import numpy as np

from prosodia.synthesis.contour import f0_for_tone, semitones_to_hz


def test_contour_length():
    f0 = f0_for_tone(2, 50)
    assert f0.shape == (50,)


def test_rising_tone_ends_higher():
    f0 = f0_for_tone(2, 64)  # 阳平, rising
    assert f0[-1] > f0[0]


def test_falling_tone_ends_lower():
    f0 = f0_for_tone(4, 64)  # 去声, falling
    assert f0[-1] < f0[0]


def test_pitch_shift_raises_whole_contour():
    low = f0_for_tone(1, 32, base_f0=200.0, pitch_shift=0.0)
    high = f0_for_tone(1, 32, base_f0=200.0, pitch_shift=12.0)
    assert np.all(high > low)
    # +12 semitones == one octave
    assert np.allclose(high, low * 2.0, rtol=1e-4)


def test_range_scales_excursion():
    narrow = f0_for_tone(4, 64, pitch_range=0.5)
    wide = f0_for_tone(4, 64, pitch_range=2.0)
    assert (wide.max() - wide.min()) > (narrow.max() - narrow.min())


def test_semitones_to_hz_octave():
    assert np.isclose(semitones_to_hz(100.0, np.array([12.0]))[0], 200.0)

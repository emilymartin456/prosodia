import numpy as np

from prosodia.synthesis.duration import phone_duration, syllable_duration
from prosodia.types import Phone, ProsodyTargets, Syllable


def test_vowel_longer_than_consonant():
    t = ProsodyTargets()
    v = phone_duration(Phone("a", is_vowel=True), t)
    c = phone_duration(Phone("t"), t)
    assert v > c


def test_rate_shortens_duration():
    slow = phone_duration(Phone("a", is_vowel=True), ProsodyTargets(rate=0.5))
    fast = phone_duration(Phone("a", is_vowel=True), ProsodyTargets(rate=2.0))
    assert slow > fast
    assert np.isclose(fast, 0.18 / 2.0)


def test_neutral_tone_shorter():
    t = ProsodyTargets()
    stressed = phone_duration(Phone("a", tone=1, is_vowel=True), t)
    neutral = phone_duration(Phone("a", tone=5, is_vowel=True), t)
    assert neutral < stressed


def test_minimum_duration_floor():
    d = phone_duration(Phone("t"), ProsodyTargets(rate=3.0))
    assert d >= 0.02


def test_syllable_sums_phones():
    syl = Syllable("ni", [Phone("n"), Phone("i", tone=3, is_vowel=True)], tone=3)
    t = ProsodyTargets()
    assert np.isclose(syllable_duration(syl, t), phone_duration(syl.phones[0], t)
                      + phone_duration(syl.phones[1], t))

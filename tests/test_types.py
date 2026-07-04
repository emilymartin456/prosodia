from prosodia.types import (
    BreakLevel,
    Language,
    Phone,
    ProsodyTargets,
    Syllable,
    Utterance,
    Word,
)


def test_break_level_pause_monotonic():
    pauses = [b.pause_seconds for b in BreakLevel]
    assert pauses == sorted(pauses)
    assert BreakLevel.NONE.pause_seconds == 0.0


def test_phone_rejects_bad_tone():
    Phone("i", tone=3, is_vowel=True)
    try:
        Phone("i", tone=9)
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("expected ValueError for tone=9")


def test_syllable_nucleus_prefers_vowel():
    syl = Syllable("ni", [Phone("n"), Phone("i", is_vowel=True)], tone=3)
    assert syl.nucleus is not None
    assert syl.nucleus.symbol == "i"


def test_utterance_flattens_words():
    syl = Syllable("hao", [Phone("h"), Phone("ao", is_vowel=True)], tone=3)
    word = Word("好", [syl], break_after=BreakLevel.SENTENCE)
    utt = Utterance("好", "好", Language.ZH, [word])
    assert utt.num_syllables == 1
    assert [p.symbol for p in utt.phones()] == ["h", "ao"]


def test_prosody_targets_clamped():
    t = ProsodyTargets(rate=10.0, pitch_shift=99.0, energy=-5.0)
    c = t.clamped()
    assert c.rate == 3.0
    assert c.pitch_shift == 12.0
    assert c.energy == 0.1

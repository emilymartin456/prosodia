import pytest

from prosodia.errors import ProsodiaError
from prosodia.expressive.emotion import get_emotion, list_emotions


def test_neutral_is_identity():
    e = get_emotion("neutral")
    assert (e.pitch_shift, e.pitch_range, e.rate, e.energy) == (0.0, 1.0, 1.0, 1.0)


def test_english_and_chinese_aliases_agree():
    assert get_emotion("happy") is get_emotion("高兴")
    assert get_emotion("开心") is get_emotion("happy")


def test_case_insensitive():
    assert get_emotion("HAPPY") is get_emotion("happy")


def test_unknown_raises():
    with pytest.raises(ProsodiaError):
        get_emotion("zesty")


def test_list_emotions_starts_with_neutral():
    names = list_emotions()
    assert names[0] == "neutral"
    assert "excited" in names

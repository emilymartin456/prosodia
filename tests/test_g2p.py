from prosodia.frontend.g2p import chinese_g2p, english_g2p, to_pinyin
from prosodia.frontend.symbols import split_initial_final


def test_to_pinyin_tone3():
    assert to_pinyin("你好") == ["ni3", "hao3"]


def test_chinese_g2p_structure():
    syls = chinese_g2p("你好")
    assert len(syls) == 2
    ni = syls[0]
    assert ni.tone == 3
    # initial "n" + final "i"
    assert [p.symbol for p in ni.phones] == ["n", "i"]
    assert ni.phones[0].is_vowel is False
    assert ni.phones[1].is_vowel is True


def test_split_initial_final():
    assert split_initial_final("zhang") == ("zh", "ang")
    assert split_initial_final("an") == ("", "an")
    assert split_initial_final("shi") == ("sh", "i")


def test_english_g2p_marks_vowels():
    syls = english_g2p("hello ok")
    assert len(syls) == 2
    symbols = [p.symbol for p in syls[0].phones]
    assert "h" in symbols
    assert any(p.is_vowel for p in syls[0].phones)

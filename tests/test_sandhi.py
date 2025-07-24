from prosodia.frontend.g2p.chinese import chinese_g2p
from prosodia.frontend.g2p.sandhi import (
    apply_bu_yi_sandhi,
    apply_sandhi,
    apply_third_tone_sandhi,
)


def tones(syllables):
    return [s.tone for s in syllables]


def test_third_tone_pair():
    syl = chinese_g2p("你好")
    apply_third_tone_sandhi(syl)
    assert tones(syl) == [2, 3]


def test_third_tone_run():
    syl = chinese_g2p("展览馆")  # zhan3 lan3 guan3
    apply_third_tone_sandhi(syl)
    assert tones(syl) == [2, 2, 3]


def test_bu_before_fourth_tone():
    syl = chinese_g2p("不是")  # bu4 shi4
    apply_bu_yi_sandhi(syl)
    assert syl[0].tone == 2


def test_yi_before_fourth_tone():
    syl = chinese_g2p("一样")  # yi1 yang4
    apply_bu_yi_sandhi(syl)
    assert syl[0].tone == 2


def test_apply_sandhi_updates_phone_tone():
    syl = chinese_g2p("你好")
    apply_sandhi(syl)
    nucleus = syl[0].nucleus
    assert nucleus is not None
    assert nucleus.tone == 2

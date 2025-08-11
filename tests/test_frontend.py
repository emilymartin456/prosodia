from prosodia.frontend import TextFrontend
from prosodia.types import BreakLevel, Language


def test_process_basic_chinese():
    utt = TextFrontend().process("你好，世界。")
    assert utt.language is Language.ZH
    # 4 characters -> 4 words
    assert len(utt.words) == 4
    assert utt.words[0].text == "你"
    # comma after 好, period after 界
    assert utt.words[1].break_after is BreakLevel.PHRASE
    assert utt.words[-1].break_after is BreakLevel.SENTENCE
    assert all(w.syllables for w in utt.words)


def test_process_normalizes_numbers():
    utt = TextFrontend(language=Language.ZH).process("共2个")
    assert "两" in utt.normalized or "二" in utt.normalized
    assert utt.normalized.startswith("共")


def test_process_applies_sandhi():
    utt = TextFrontend().process("你好")
    assert utt.words[0].syllables[0].tone == 2  # 3-3 sandhi


def test_process_without_normalization():
    utt = TextFrontend(normalize=False).process("你好")
    assert utt.normalized == "你好"


def test_phones_flatten():
    utt = TextFrontend().process("你好")
    assert len(utt.phones()) >= 2

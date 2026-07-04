from prosodia.frontend.normalize.pipeline import Normalizer, detect_language
from prosodia.types import Language


def test_detect_language():
    assert detect_language("你好") is Language.ZH
    assert detect_language("hello 123") is Language.EN


def test_zh_date_and_time():
    n = Normalizer(Language.ZH)
    assert n.normalize("2026年7月5日") == "二零二六年七月五日"
    assert "三点半" in n.normalize("会议在3:30开始")


def test_zh_standalone_number():
    n = Normalizer(Language.ZH)
    assert n.normalize("共105人") == "共一百零五人"


def test_english_numbers_and_money():
    n = Normalizer(Language.EN)
    assert n.normalize("I have 3 apples") == "I have three apples"
    assert "five dollars" in n.normalize("it costs $5")


def test_auto_dispatch():
    n = Normalizer()
    assert "一百" in n.normalize("有100个")
    assert "three" in n.normalize("just 3 things")

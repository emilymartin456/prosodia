from prosodia.frontend.normalize.numbers_zh import (
    read_cardinal,
    read_decimal,
    read_digits,
)


def test_read_digits():
    assert read_digits("2026") == "二零二六"
    assert read_digits("100") == "一零零"


def test_read_cardinal_small():
    assert read_cardinal(0) == "零"
    assert read_cardinal(5) == "五"
    assert read_cardinal(10) == "十"
    assert read_cardinal(11) == "十一"
    assert read_cardinal(20) == "二十"
    assert read_cardinal(21) == "二十一"


def test_read_cardinal_hundreds_and_zero():
    assert read_cardinal(100) == "一百"
    assert read_cardinal(105) == "一百零五"
    assert read_cardinal(110) == "一百一十"
    assert read_cardinal(200) == "两百"


def test_read_cardinal_thousands():
    assert read_cardinal(1000) == "一千"
    assert read_cardinal(2026) == "两千零二十六"
    assert read_cardinal(10005) == "一万零五"


def test_read_cardinal_negative():
    assert read_cardinal(-3) == "负三"


def test_read_decimal():
    assert read_decimal("3.14") == "三点一四"
    assert read_decimal("0.5") == "零点五"
    assert read_decimal("42") == "四十二"

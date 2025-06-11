from prosodia.frontend.normalize.numbers_en import read_cardinal, read_decimal


def test_read_cardinal_small():
    assert read_cardinal(0) == "zero"
    assert read_cardinal(5) == "five"
    assert read_cardinal(19) == "nineteen"
    assert read_cardinal(21) == "twenty-one"


def test_read_cardinal_hundreds():
    assert read_cardinal(100) == "one hundred"
    assert read_cardinal(105) == "one hundred and five"
    assert read_cardinal(342) == "three hundred and forty-two"


def test_read_cardinal_large():
    assert read_cardinal(2026) == "two thousand and twenty-six"
    assert read_cardinal(1_000_000) == "one million"


def test_read_cardinal_negative():
    assert read_cardinal(-7) == "minus seven"


def test_read_decimal():
    assert read_decimal("3.14") == "three point one four"
    assert read_decimal("42") == "forty-two"

from prosodia.frontend.normalize.units import normalize_units


def test_currency():
    assert normalize_units("$5") == "五美元"
    assert normalize_units("¥3.5") == "三点五元"
    assert normalize_units("£100") == "一百英镑"


def test_percent():
    assert normalize_units("5%") == "百分之五"
    assert normalize_units("12.5%") == "百分之十二点五"


def test_units():
    assert normalize_units("5km") == "五千米"
    assert normalize_units("37℃") == "三十七摄氏度"
    assert normalize_units("250 g") == "两百五十克"


def test_leaves_plain_text():
    assert normalize_units("你好世界") == "你好世界"

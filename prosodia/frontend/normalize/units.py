"""Normalize currency amounts, percentages and measurement units (Mandarin)."""

from __future__ import annotations

import re

from prosodia.frontend.normalize.numbers_zh import read_decimal

_NUM = r"\d+(?:\.\d+)?"

_CURRENCY = {"¥": "元", "￥": "元", "$": "美元", "€": "欧元", "£": "英镑"}
_UNITS = {
    "km": "千米",
    "cm": "厘米",
    "mm": "毫米",
    "kg": "千克",
    "℃": "摄氏度",
    "°C": "摄氏度",
    "m": "米",
    "g": "克",
}

_CURRENCY_RE = re.compile(r"(-?)([¥￥$€£])(" + _NUM + r")")
_PERCENT_RE = re.compile(r"(-?)(" + _NUM + r")%")
_PERMILLE_RE = re.compile(r"(-?)(" + _NUM + r")‰")
_UNIT_RE = re.compile(r"(-?)(" + _NUM + r")\s*(km|kg|cm|mm|℃|°C|m|g)")


def _read(sign: str, number: str) -> str:
    body = read_decimal(number)
    return ("负" + body) if sign == "-" else body


def _read_ratio(prefix: str, sign: str, number: str) -> str:
    # "-5%" reads as "负百分之五", not "百分之负五".
    body = f"{prefix}{read_decimal(number)}"
    return ("负" + body) if sign == "-" else body


def normalize_units(text: str) -> str:
    text = _CURRENCY_RE.sub(lambda m: _read(m.group(1), m.group(3)) + _CURRENCY[m.group(2)], text)
    text = _PERCENT_RE.sub(lambda m: _read_ratio("百分之", m.group(1), m.group(2)), text)
    text = _PERMILLE_RE.sub(lambda m: _read_ratio("千分之", m.group(1), m.group(2)), text)
    text = _UNIT_RE.sub(lambda m: _read(m.group(1), m.group(2)) + _UNITS[m.group(3)], text)
    return text

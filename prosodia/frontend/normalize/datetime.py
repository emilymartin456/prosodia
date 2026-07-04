"""Normalize Chinese dates and clock times to their spoken reading.

Years are read digit-by-digit (``2026年`` -> ``二零二六年``) while months, days and
clock components are read as cardinals, matching how the dates are actually
spoken.
"""

from __future__ import annotations

import re

from prosodia.frontend.normalize.numbers_zh import read_cardinal, read_digits

_FULL_DATE = re.compile(r"(\d{4})\s*[-/年]\s*(\d{1,2})\s*[-/月]\s*(\d{1,2})\s*日?")
_YEAR_MONTH = re.compile(r"(\d{4})年(\d{1,2})月")
_YEAR = re.compile(r"(\d{4})年")
_MONTH_DAY = re.compile(r"(\d{1,2})月(\d{1,2})日")
_TIME = re.compile(r"(\d{1,2}):(\d{2})")


def _read_ymd(year: str, month: str, day: str) -> str:
    return f"{read_digits(year)}年{read_cardinal(int(month))}月{read_cardinal(int(day))}日"


def _time_repl(match: re.Match) -> str:
    hour, minute = int(match.group(1)), int(match.group(2))
    if minute == 0:
        return f"{read_cardinal(hour)}点"
    if minute == 30:
        return f"{read_cardinal(hour)}点半"
    return f"{read_cardinal(hour)}点{read_cardinal(minute)}分"


def normalize_datetime(text: str) -> str:
    text = _FULL_DATE.sub(lambda m: _read_ymd(*m.groups()), text)
    text = _YEAR_MONTH.sub(
        lambda m: f"{read_digits(m.group(1))}年{read_cardinal(int(m.group(2)))}月", text
    )
    text = _YEAR.sub(lambda m: f"{read_digits(m.group(1))}年", text)
    text = _MONTH_DAY.sub(
        lambda m: f"{read_cardinal(int(m.group(1)))}月{read_cardinal(int(m.group(2)))}日",
        text,
    )
    text = _TIME.sub(_time_repl, text)
    return text

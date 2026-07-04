"""Expand Arabic numerals to English words.

A compact hand-rolled expander (no ``inflect`` dependency) covering cardinals up
to the billions plus decimals — enough for the numbers a TTS frontend meets in
running text.
"""

from __future__ import annotations

_ONES = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
)
_TENS = (
    "",
    "",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
)
_SCALES = (("", 1), ("thousand", 1_000), ("million", 1_000_000), ("billion", 1_000_000_000))


def _read_below_100(n: int) -> str:
    if n < 20:
        return _ONES[n]
    tens, ones = divmod(n, 10)
    return _TENS[tens] + (f"-{_ONES[ones]}" if ones else "")


def _read_below_1000(n: int) -> str:
    hundreds, rest = divmod(n, 100)
    parts = []
    if hundreds:
        parts.append(f"{_ONES[hundreds]} hundred")
    if rest:
        if hundreds:
            parts.append("and")
        parts.append(_read_below_100(rest))
    return " ".join(parts)


def read_cardinal(n: int) -> str:
    """Read ``n`` as English words, e.g. ``2026 -> "two thousand and twenty-six"``."""
    if n < 0:
        return "minus " + read_cardinal(-n)
    if n == 0:
        return "zero"

    groups: list[int] = []
    while n > 0:
        groups.append(n % 1000)
        n //= 1000

    chunks: list[str] = []
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if g == 0:
            continue
        name = _SCALES[i][0]
        segment = _read_below_1000(g)
        chunks.append(f"{segment} {name}".strip())
    text = " ".join(chunks)
    # Idiomatic "and" before a bare sub-hundred remainder ("... thousand and five").
    if len(groups) > 1 and 0 < groups[0] < 100:
        head, _, tail = text.rpartition(" ")
        if head:
            text = f"{head} and {tail}"
    return text


def read_decimal(text: str) -> str:
    """Read a decimal string, e.g. ``"3.14" -> "three point one four"``."""
    if "." not in text:
        return read_cardinal(int(text))
    int_part, frac_part = text.split(".", 1)
    head = read_cardinal(int(int_part)) if int_part else "zero"
    tail = " ".join(_ONES[int(c)] for c in frac_part if c.isdigit())
    return f"{head} point {tail}"

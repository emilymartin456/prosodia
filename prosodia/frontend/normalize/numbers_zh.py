"""Convert Arabic numerals to their spoken Mandarin reading.

Three readings are exposed because context decides which one a TTS frontend
wants:

* :func:`read_cardinal` — quantity reading (``2026`` -> ``两千零二十六``);
* :func:`read_digits` — digit-by-digit (``2026`` -> ``二零二六``), used for years,
  phone numbers and other identifiers;
* :func:`read_decimal` — cardinal integer part + ``点`` + digit-by-digit fraction.
"""

from __future__ import annotations

_DIGITS = "零一二三四五六七八九"
_SMALL_UNITS = ("", "十", "百", "千")
_BIG_UNITS = ("", "万", "亿", "兆")


def read_digits(text: str) -> str:
    """Read each Arabic digit on its own, e.g. ``"2026" -> "二零二六"``."""
    return "".join(_DIGITS[int(c)] if c.isdigit() else c for c in text)


def _read_below_10000(n: int) -> str:
    """Read 0 <= n < 10000 without the group's big unit."""
    if n == 0:
        return ""
    out: list[str] = []
    pending_zero = False
    for pos in range(3, -1, -1):
        unit = 10**pos
        digit = (n // unit) % 10
        if digit == 0:
            # Remember we skipped a zero so a single 零 can be emitted later.
            if out:
                pending_zero = True
            continue
        if pending_zero:
            out.append(_DIGITS[0])
            pending_zero = False
        # "两" reads more naturally than "二" before 百/千.
        if digit == 2 and pos >= 2:
            out.append("两")
        else:
            out.append(_DIGITS[digit])
        out.append(_SMALL_UNITS[pos])
    text = "".join(out)
    # 一十… -> 十… (十一 not 一十一) only at the very front.
    if text.startswith("一十"):
        text = text[1:]
    return text


def read_cardinal(n: int) -> str:
    """Read ``n`` as a Mandarin quantity, e.g. ``105 -> 一百零五``."""
    if n < 0:
        return "负" + read_cardinal(-n)
    if n == 0:
        return _DIGITS[0]

    groups: list[int] = []
    while n > 0:
        groups.append(n % 10000)
        n //= 10000

    parts: list[str] = []
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if g == 0:
            continue
        seg = _read_below_10000(g)
        # A group below 1000 that is not the most significant needs a leading 零
        # ("一万零五百" would be wrong; but "一万零五" needs the 零).
        if parts and g < 1000:
            parts.append(_DIGITS[0])
        parts.append(seg + _BIG_UNITS[i])
    return "".join(parts)


def read_decimal(text: str) -> str:
    """Read a decimal string, e.g. ``"3.14" -> "三点一四"``."""
    if "." not in text:
        return read_cardinal(int(text))
    int_part, frac_part = text.split(".", 1)
    head = read_cardinal(int(int_part)) if int_part else _DIGITS[0]
    # A trailing dot with no fraction ("5.") should not leave a dangling 点.
    if not frac_part:
        return head
    return f"{head}点{read_digits(frac_part)}"

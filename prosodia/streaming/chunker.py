"""Split long text into synthesizable chunks at natural boundaries.

For low first-audio latency the engine synthesizes one chunk at a time, so chunks
should end on sentence (then phrase) boundaries and stay under a character
budget. Oversized single phrases are hard-split as a last resort.
"""

from __future__ import annotations

_SENTENCE_END = "。！？!?…\n"
_PHRASE_END = "，,、;；:："


def _split_keeping_delims(text: str, delimiters: str) -> list[str]:
    chunks: list[str] = []
    buf: list[str] = []
    for ch in text:
        buf.append(ch)
        if ch in delimiters:
            chunks.append("".join(buf))
            buf = []
    if buf:
        chunks.append("".join(buf))
    return [c for c in chunks if c.strip()]


def chunk_text(text: str, max_chars: int = 60) -> list[str]:
    """Break ``text`` into chunks of at most ``max_chars`` characters."""
    if max_chars < 1:
        raise ValueError("max_chars must be >= 1")
    text = text.strip()
    if not text:
        return []

    packed: list[str] = []
    for sentence in _split_keeping_delims(text, _SENTENCE_END):
        sentence = sentence.strip()
        if len(sentence) <= max_chars:
            packed.append(sentence)
            continue
        buf = ""
        for phrase in _split_keeping_delims(sentence, _PHRASE_END):
            if buf and len(buf) + len(phrase) > max_chars:
                packed.append(buf.strip())
                buf = phrase
            else:
                buf += phrase
        if buf.strip():
            packed.append(buf.strip())

    # Hard-split anything still over budget (e.g. a very long unpunctuated run).
    result: list[str] = []
    for chunk in packed:
        while len(chunk) > max_chars:
            result.append(chunk[:max_chars])
            chunk = chunk[max_chars:]
        if chunk:
            result.append(chunk)
    return result

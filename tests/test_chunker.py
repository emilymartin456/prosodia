import pytest

from prosodia.streaming.chunker import chunk_text


def test_short_text_single_chunk():
    assert chunk_text("你好世界") == ["你好世界"]


def test_empty_text():
    assert chunk_text("") == []
    assert chunk_text("   ") == []


def test_splits_by_sentence():
    chunks = chunk_text("你好。世界。今天好。", max_chars=100)
    assert chunks == ["你好。", "世界。", "今天好。"]


def test_respects_max_chars():
    text = "，".join(["短语"] * 20)  # long, comma-separated
    chunks = chunk_text(text, max_chars=10)
    assert all(len(c) <= 10 for c in chunks)
    assert len(chunks) > 1


def test_hard_split_unpunctuated():
    text = "字" * 25
    chunks = chunk_text(text, max_chars=10)
    assert all(len(c) <= 10 for c in chunks)
    assert "".join(chunks) == text


def test_bad_max_chars():
    with pytest.raises(ValueError):
        chunk_text("x", max_chars=0)

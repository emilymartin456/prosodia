"""Prompt templates and response parsing for model-backed adapters.

The templates ask the model to return strict JSON so the response can be parsed
deterministically. They are intentionally few-shot and compact to keep token
cost and latency low on the hot path.
"""

from __future__ import annotations

import json

from prosodia.errors import AdapterError
from prosodia.llm.base import ProsodyPrediction

NORMALIZE_SYSTEM = (
    "你是一个语音合成前端的文本规范化模块。"
    "把输入文本改写成朗读时应当念出的形式："
    "数字、日期、金额、单位、符号都要展开成口语读法。"
    "只返回改写后的纯文本，不要解释。"
)

PROSODY_SYSTEM = (
    "你是一个语音合成前端的韵律预测模块。"
    "把输入文本切分成自然的韵律短语，并标出需要重读的词。"
    '严格返回 JSON：{"phrases": [...], "emphasis": [...]}，不要其他文字。'
)


def build_normalize_messages(text: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": NORMALIZE_SYSTEM},
        {"role": "user", "content": text},
    ]


def build_prosody_messages(text: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": PROSODY_SYSTEM},
        {"role": "user", "content": text},
    ]


def parse_prosody_json(raw: str) -> ProsodyPrediction:
    """Parse a model's JSON reply into a :class:`ProsodyPrediction`."""
    raw = raw.strip()
    # Tolerate a fenced ```json block.
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw[raw.find("{") : raw.rfind("}") + 1]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AdapterError(f"model returned invalid JSON: {exc}") from exc
    phrases = data.get("phrases")
    if not isinstance(phrases, list) or not all(isinstance(p, str) for p in phrases):
        raise AdapterError("'phrases' must be a list of strings")
    emphasis = tuple(str(w) for w in data.get("emphasis", []))
    return ProsodyPrediction(phrases=phrases, emphasis=emphasis)

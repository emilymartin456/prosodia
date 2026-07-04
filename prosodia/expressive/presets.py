"""Named style presets for common speaking scenarios."""

from __future__ import annotations

from dataclasses import replace

from prosodia.errors import ProsodiaError
from prosodia.expressive.style import StyleControl

_PRESETS: dict[str, StyleControl] = {
    # 新闻播报: measured, slightly faster, formal.
    "news": StyleControl(emotion="serious", intensity=0.8, rate=1.05),
    # 讲故事: gentle, unhurried, longer pauses.
    "storytelling": StyleControl(emotion="gentle", intensity=1.0, rate=0.95, pause_scale=1.3),
    # 语音助手: calm and even.
    "assistant": StyleControl(emotion="calm", intensity=0.7),
    # 客服: warm and polite.
    "customer_service": StyleControl(emotion="gentle", intensity=0.9),
    # 广告: upbeat and loud.
    "advertisement": StyleControl(emotion="excited", intensity=1.2, energy=1.1),
    # 诗朗诵: slow, spacious.
    "poetry": StyleControl(emotion="calm", intensity=1.0, rate=0.85, pause_scale=1.5),
}

_ALIASES = {
    "新闻": "news",
    "播报": "news",
    "讲故事": "storytelling",
    "故事": "storytelling",
    "助手": "assistant",
    "客服": "customer_service",
    "广告": "advertisement",
    "诗朗诵": "poetry",
}


def get_preset(name: str) -> StyleControl:
    """Return a fresh copy of a named preset (safe to mutate)."""
    key = _ALIASES.get(name, name)
    if key not in _PRESETS:
        raise ProsodiaError(f"unknown preset: {name!r}; try one of {list_presets()}")
    return replace(_PRESETS[key])


def list_presets() -> list[str]:
    return list(_PRESETS)

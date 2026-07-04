"""Language-model adapters for text normalization and prosody prediction.

The default :class:`~prosodia.llm.rulebased.RuleBasedAdapter` is fully offline;
:class:`~prosodia.llm.openai_compat.OpenAICompatibleAdapter` calls an
OpenAI-compatible chat endpoint when one is configured. Both satisfy the same
:class:`~prosodia.llm.base.LLMAdapter` interface, so the pipeline treats them
interchangeably.
"""

from __future__ import annotations

from prosodia.llm.base import LLMAdapter, ProsodyPrediction

__all__ = ["LLMAdapter", "ProsodyPrediction"]

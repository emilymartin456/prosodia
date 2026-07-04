"""An adapter that calls an OpenAI-compatible chat completions endpoint.

The network call is isolated behind a ``chat_fn`` callable so the adapter can be
unit-tested with a fake transport and used against any OpenAI-compatible server
(OpenAI, a local vLLM, etc.). When no ``chat_fn`` is supplied one is built lazily
from the ``openai`` SDK, which is only needed at call time.
"""

from __future__ import annotations

from collections.abc import Callable

from prosodia.errors import AdapterError
from prosodia.llm.base import LLMAdapter, ProsodyPrediction
from prosodia.llm.prompts import (
    build_normalize_messages,
    build_prosody_messages,
    parse_prosody_json,
)
from prosodia.types import Language

ChatFn = Callable[[list[dict[str, str]]], str]


class OpenAICompatibleAdapter(LLMAdapter):
    name = "openai"

    def __init__(
        self,
        chat_fn: ChatFn | None = None,
        *,
        model: str = "gpt-4o-mini",
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.model = model
        self._chat_fn = chat_fn or self._build_default_chat_fn(base_url, api_key)

    def normalize(self, text: str, language: Language = Language.AUTO) -> str:
        reply = self._chat_fn(build_normalize_messages(text))
        return reply.strip()

    def predict_prosody(self, text: str, language: Language = Language.AUTO) -> ProsodyPrediction:
        reply = self._chat_fn(build_prosody_messages(text))
        return parse_prosody_json(reply)

    def _build_default_chat_fn(self, base_url: str | None, api_key: str | None) -> ChatFn:
        def chat_fn(messages: list[dict[str, str]]) -> str:
            try:
                from openai import OpenAI
            except ModuleNotFoundError as exc:  # pragma: no cover - optional dep
                raise AdapterError(
                    "the openai adapter needs the openai SDK; install prosodia[llm]"
                ) from exc
            client = OpenAI(base_url=base_url, api_key=api_key)
            response = client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.0
            )
            return response.choices[0].message.content or ""

        return chat_fn

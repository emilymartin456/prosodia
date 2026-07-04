"""The one-call facade: :class:`ExpressiveTTS`.

This ties the stages together — frontend, expressive control, synthesis backend —
behind ``say`` and ``stream``. An optional :class:`~prosodia.llm.base.LLMAdapter`
handles text normalization (and, when present, turns off the rule-based frontend
normalizer so the two do not both fire).
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path

from prosodia.audio.chunk import AudioChunk
from prosodia.audio.wav import write_wav
from prosodia.config import Config
from prosodia.expressive.style import StyleControl
from prosodia.frontend import TextFrontend
from prosodia.llm.base import LLMAdapter
from prosodia.streaming.engine import StreamingEngine
from prosodia.streaming.metrics import StreamStats
from prosodia.synthesis.backends import get_backend
from prosodia.synthesis.backends.base import AcousticBackend
from prosodia.synthesis.plan import build_plan
from prosodia.types import Utterance


class ExpressiveTTS:
    """High-level expressive text-to-speech."""

    def __init__(
        self,
        config: Config | None = None,
        backend: AcousticBackend | None = None,
        adapter: LLMAdapter | None = None,
    ) -> None:
        self.config = (config or Config()).validate()
        self.adapter = adapter
        # When an adapter normalizes text, the frontend must not normalize again.
        frontend_normalize = self.config.frontend.normalize and adapter is None
        self.frontend = TextFrontend(
            language=self.config.frontend.language, normalize=frontend_normalize
        )
        self.backend = backend or get_backend(self.config.synthesis.backend)

    # -- helpers ---------------------------------------------------------
    def _resolve_style(
        self,
        emotion: str | None,
        style: StyleControl | None,
        overrides: dict[str, float | None],
    ) -> StyleControl:
        if style is not None:
            base = replace(style)
        else:
            base = StyleControl(
                emotion=emotion or self.config.expressive.emotion,
                intensity=self.config.expressive.intensity,
                base_f0=self.config.expressive.base_f0,
            )
        for key, value in overrides.items():
            if value is not None:
                setattr(base, key, value)
        return base

    def _prepare_text(self, text: str) -> str:
        if self.adapter is not None:
            return self.adapter.normalize(text, self.config.frontend.language)
        return text

    # -- public ----------------------------------------------------------
    def analyze(self, text: str) -> Utterance:
        """Run only the frontend and return the analysed utterance."""
        return self.frontend.process(self._prepare_text(text))

    def say(
        self,
        text: str,
        emotion: str | None = None,
        *,
        style: StyleControl | None = None,
        rate: float | None = None,
        pitch_shift: float | None = None,
        energy: float | None = None,
        intensity: float | None = None,
    ) -> AudioChunk:
        """Synthesize ``text`` into a single :class:`AudioChunk`."""
        resolved = self._resolve_style(
            emotion,
            style,
            {
                "rate": rate,
                "pitch_shift": pitch_shift,
                "energy": energy,
                "intensity": intensity,
            },
        )
        utterance = self.frontend.process(self._prepare_text(text))
        plan = build_plan(utterance, resolved, self.config.audio.sample_rate)
        return self.backend.render(plan)

    def to_wav(self, text: str, path: str | Path, **kwargs: object) -> AudioChunk:
        """Synthesize and write a WAV file, returning the rendered audio."""
        chunk = self.say(text, **kwargs)  # type: ignore[arg-type]
        write_wav(path, chunk)
        return chunk

    def _engine(self, resolved: StyleControl) -> StreamingEngine:
        return StreamingEngine(
            frontend=self.frontend,
            backend=self.backend,
            style=resolved,
            sample_rate=self.config.audio.sample_rate,
            max_chunk_chars=self.config.streaming.max_chunk_chars,
        )

    def stream(
        self,
        text: str,
        emotion: str | None = None,
        *,
        style: StyleControl | None = None,
        rate: float | None = None,
        pitch_shift: float | None = None,
        energy: float | None = None,
        intensity: float | None = None,
    ) -> Iterator[AudioChunk]:
        """Yield audio chunks as each piece of ``text`` is synthesized."""
        resolved = self._resolve_style(
            emotion,
            style,
            {
                "rate": rate,
                "pitch_shift": pitch_shift,
                "energy": energy,
                "intensity": intensity,
            },
        )
        return self._engine(resolved).stream(self._prepare_text(text))

    def stream_to_wav(self, text: str, path: str | Path, **kwargs: object) -> StreamStats:
        """Stream-synthesize ``text`` straight to a WAV file, returning stats."""
        resolved = self._resolve_style(
            kwargs.get("emotion"),  # type: ignore[arg-type]
            kwargs.get("style"),  # type: ignore[arg-type]
            {
                "rate": kwargs.get("rate"),  # type: ignore[dict-item]
                "pitch_shift": kwargs.get("pitch_shift"),  # type: ignore[dict-item]
                "energy": kwargs.get("energy"),  # type: ignore[dict-item]
                "intensity": kwargs.get("intensity"),  # type: ignore[dict-item]
            },
        )
        audio, stats = self._engine(resolved).run(self._prepare_text(text))
        write_wav(path, audio)
        return stats

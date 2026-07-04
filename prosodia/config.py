"""Typed configuration for the whole pipeline.

Every stage takes its slice of :class:`Config`. Defaults are chosen so that
``Config()`` produces a working, fully offline setup (rule-based frontend,
reference backend). :meth:`Config.validate` catches inconsistent values early
instead of letting them blow up deep inside synthesis.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields

from prosodia.errors import ConfigError
from prosodia.types import Language


@dataclass
class AudioConfig:
    sample_rate: int = 22050
    n_channels: int = 1


@dataclass
class FrontendConfig:
    language: Language = Language.AUTO
    normalize: bool = True
    predict_prosody: bool = True
    # Adapter used for normalization / prosody. "rule" is fully offline.
    adapter: str = "rule"


@dataclass
class ExpressiveConfig:
    emotion: str = "neutral"
    intensity: float = 1.0
    base_f0: float = 200.0


@dataclass
class SynthesisConfig:
    backend: str = "reference"
    # Frames rendered per synthesis block; also the streaming granularity.
    block_ms: int = 40


@dataclass
class StreamingConfig:
    max_chunk_chars: int = 60
    lookahead_chunks: int = 1


@dataclass
class Config:
    audio: AudioConfig = field(default_factory=AudioConfig)
    frontend: FrontendConfig = field(default_factory=FrontendConfig)
    expressive: ExpressiveConfig = field(default_factory=ExpressiveConfig)
    synthesis: SynthesisConfig = field(default_factory=SynthesisConfig)
    streaming: StreamingConfig = field(default_factory=StreamingConfig)

    def validate(self) -> Config:
        if self.audio.sample_rate <= 0:
            raise ConfigError("audio.sample_rate must be positive")
        if self.audio.n_channels != 1:
            raise ConfigError("only mono (n_channels=1) is supported")
        if not 0.0 <= self.expressive.intensity <= 3.0:
            raise ConfigError("expressive.intensity must be in 0..3")
        if self.streaming.max_chunk_chars < 1:
            raise ConfigError("streaming.max_chunk_chars must be >= 1")
        if self.synthesis.block_ms < 1:
            raise ConfigError("synthesis.block_ms must be >= 1")
        return self

    def to_dict(self) -> dict:
        d = asdict(self)
        d["frontend"]["language"] = self.frontend.language.value
        return d

    @classmethod
    def from_dict(cls, data: dict) -> Config:
        """Build a Config from a (possibly partial) nested dict."""
        section_types = {f.name: f.type for f in fields(cls)}
        kwargs: dict = {}
        for name, sub_cls in _SECTIONS.items():
            raw = data.get(name, {})
            if not isinstance(raw, dict):
                raise ConfigError(f"section '{name}' must be a mapping")
            if name == "frontend" and "language" in raw:
                raw = {**raw, "language": Language(raw["language"])}
            allowed = {f.name for f in fields(sub_cls)}
            unknown = set(raw) - allowed
            if unknown:
                raise ConfigError(f"unknown keys in '{name}': {sorted(unknown)}")
            kwargs[name] = sub_cls(**raw)
        _ = section_types  # kept for future schema introspection
        return cls(**kwargs).validate()


_SECTIONS = {
    "audio": AudioConfig,
    "frontend": FrontendConfig,
    "expressive": ExpressiveConfig,
    "synthesis": SynthesisConfig,
    "streaming": StreamingConfig,
}

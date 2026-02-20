"""The adapter interface between prosodia and a language model.

An adapter does two jobs for the frontend: rewrite text into its spoken form
(:meth:`normalize`) and segment it into prosodic phrases with optional emphasis
(:meth:`predict_prosody`). Keeping the surface this small means a rule-based
implementation and a networked model implementation are genuinely swappable.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from prosodia.types import Language


@dataclass
class ProsodyPrediction:
    """Structured prosody guidance for one input."""

    phrases: list[str]
    emphasis: tuple[str, ...] = field(default_factory=tuple)

    @property
    def num_phrases(self) -> int:
        return len(self.phrases)


class LLMAdapter(ABC):
    """Normalize text and predict prosody, backed by rules or a model."""

    name: str = "base"

    @abstractmethod
    def normalize(self, text: str, language: Language = Language.AUTO) -> str:
        """Return the spoken-form reading of ``text``."""

    @abstractmethod
    def predict_prosody(self, text: str, language: Language = Language.AUTO) -> ProsodyPrediction:
        """Return prosodic phrasing and emphasis for ``text``."""

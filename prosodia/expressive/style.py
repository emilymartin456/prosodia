"""Style vectors and the high-level :class:`StyleControl`.

A :class:`StyleVector` is the raw numeric knob set (rate, pitch shift, pitch
range, energy, pause scale). :class:`StyleControl` is the user-facing request —
an emotion plus an intensity plus optional manual overrides — that resolves down
to :class:`~prosodia.types.ProsodyTargets` for the synthesis stage.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StyleVector:
    """A multiplicative/additive bundle of prosody knobs."""

    rate: float = 1.0
    pitch_shift: float = 0.0
    pitch_range: float = 1.0
    energy: float = 1.0
    pause_scale: float = 1.0

    def blend(self, other: StyleVector, weight: float) -> StyleVector:
        """Linearly interpolate towards ``other`` by ``weight`` in [0, 1]."""
        w = max(0.0, min(1.0, weight))

        def mix(a: float, b: float) -> float:
            return a * (1.0 - w) + b * w

        return StyleVector(
            rate=mix(self.rate, other.rate),
            pitch_shift=mix(self.pitch_shift, other.pitch_shift),
            pitch_range=mix(self.pitch_range, other.pitch_range),
            energy=mix(self.energy, other.energy),
            pause_scale=mix(self.pause_scale, other.pause_scale),
        )

    def combine(self, other: StyleVector) -> StyleVector:
        """Stack another vector on top: multipliers multiply, shifts add."""
        return StyleVector(
            rate=self.rate * other.rate,
            pitch_shift=self.pitch_shift + other.pitch_shift,
            pitch_range=self.pitch_range * other.pitch_range,
            energy=self.energy * other.energy,
            pause_scale=self.pause_scale * other.pause_scale,
        )


@dataclass
class StyleControl:
    """A user request for expressive speech."""

    emotion: str = "neutral"
    intensity: float = 1.0
    # Manual overrides layered on top of the emotion.
    rate: float = 1.0
    pitch_shift: float = 0.0
    energy: float = 1.0
    pause_scale: float = 1.0
    base_f0: float = 200.0

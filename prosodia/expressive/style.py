"""Style vectors and the high-level :class:`StyleControl`.

A :class:`StyleVector` is the raw numeric knob set (rate, pitch shift, pitch
range, energy, pause scale). :class:`StyleControl` is the user-facing request —
an emotion plus an intensity plus optional manual overrides — that resolves down
to :class:`~prosodia.types.ProsodyTargets` for the synthesis stage.
"""

from __future__ import annotations

from dataclasses import dataclass

from prosodia.types import ProsodyTargets


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

    def to_vector(self) -> StyleVector:
        """Resolve emotion + intensity + overrides into one style vector.

        Intensity scales each emotion delta linearly (intensity 0 == neutral),
        then the manual overrides are stacked on top with :meth:`StyleVector.combine`.
        """
        from prosodia.expressive.emotion import get_emotion

        emo = get_emotion(self.emotion)
        k = max(0.0, min(3.0, self.intensity))
        emotion_vec = StyleVector(
            rate=1.0 + (emo.rate - 1.0) * k,
            pitch_shift=emo.pitch_shift * k,
            pitch_range=1.0 + (emo.pitch_range - 1.0) * k,
            energy=1.0 + (emo.energy - 1.0) * k,
        )
        override_vec = StyleVector(
            rate=self.rate,
            pitch_shift=self.pitch_shift,
            energy=self.energy,
            pause_scale=self.pause_scale,
        )
        return emotion_vec.combine(override_vec)

    def to_targets(self) -> ProsodyTargets:
        """Produce clamped :class:`ProsodyTargets` for the synthesis stage."""
        v = self.to_vector()
        return ProsodyTargets(
            rate=v.rate,
            pitch_shift=v.pitch_shift,
            pitch_range=v.pitch_range,
            energy=v.energy,
            pause_scale=v.pause_scale,
            base_f0=self.base_f0,
        ).clamped()

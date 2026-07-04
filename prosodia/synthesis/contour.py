"""Generate F0 (pitch) contours from Mandarin tone shapes.

Each tone is described by a handful of control points in semitones relative to
the syllable's base pitch. The contour is interpolated to the requested number
of frames, scaled by ``pitch_range`` and shifted by ``pitch_shift``, then
converted from semitones back to Hz.
"""

from __future__ import annotations

import numpy as np

# Relative semitone control points per Chinese tone (Chao tone-letter inspired).
TONE_SHAPES: dict[int, tuple[float, ...]] = {
    0: (0.0, 0.0),  # unknown / atonal
    1: (4.0, 4.0),  # high level ˥
    2: (-1.0, 5.0),  # rising ˧˥
    3: (-2.0, -4.0, 0.0),  # low dipping ˨˩˦
    4: (5.0, -3.0),  # falling ˥˩
    5: (0.0, -1.0),  # neutral, short
}


def semitones_to_hz(base_hz: float, semitones: np.ndarray) -> np.ndarray:
    return base_hz * np.power(2.0, semitones / 12.0)


def f0_for_tone(
    tone: int,
    n_frames: int,
    base_f0: float = 200.0,
    pitch_shift: float = 0.0,
    pitch_range: float = 1.0,
) -> np.ndarray:
    """Return an ``n_frames`` F0 track (Hz) for a single toned syllable."""
    n_frames = max(1, n_frames)
    shape = np.asarray(TONE_SHAPES.get(tone, TONE_SHAPES[0]), dtype=np.float64)
    if shape.size == 1:
        semis = np.full(n_frames, shape[0])
    else:
        xs = np.linspace(0.0, shape.size - 1, n_frames)
        semis = np.interp(xs, np.arange(shape.size), shape)
    semis = semis * pitch_range + pitch_shift
    return semitones_to_hz(base_f0, semis).astype(np.float32)

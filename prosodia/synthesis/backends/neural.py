"""Extension point for a neural acoustic backend.

The framework is designed so a trained vocoder/acoustic model can drop in behind
:class:`~prosodia.synthesis.backends.base.AcousticBackend`. This module holds a
concrete slot for a torch-based model; importing torch is deferred so the core
package stays dependency-light and installs without a deep-learning stack.
"""

from __future__ import annotations

import numpy as np

from prosodia.errors import BackendNotAvailable
from prosodia.synthesis.backends.base import AcousticBackend
from prosodia.synthesis.plan import Segment


class NeuralBackend(AcousticBackend):
    """Adapter for a torch checkpoint (weights supplied by the user).

    Instantiation fails fast with :class:`BackendNotAvailable` when torch is not
    installed, so callers get a clear message instead of an ``ImportError`` deep
    inside synthesis.
    """

    name = "neural"

    def __init__(self, checkpoint: str | None = None) -> None:
        try:
            import torch  # noqa: F401
        except ModuleNotFoundError as exc:  # pragma: no cover - optional dep
            raise BackendNotAvailable(
                "the neural backend needs torch; install prosodia[neural]"
            ) from exc
        self.checkpoint = checkpoint

    def render_segment(self, segment: Segment, sample_rate: int) -> np.ndarray:  # pragma: no cover
        raise NotImplementedError(
            "NeuralBackend is an extension point; load a checkpoint to enable rendering"
        )

import numpy as np
import pytest

from prosodia.errors import BackendError
from prosodia.synthesis.backends import (
    AcousticBackend,
    available_backends,
    get_backend,
    register_backend,
)
from prosodia.synthesis.backends.reference import FormantSynthBackend
from prosodia.synthesis.plan import Segment


def test_reference_is_registered():
    assert "reference" in available_backends()
    assert isinstance(get_backend("reference"), FormantSynthBackend)


def test_neural_is_registered_even_without_torch():
    # The factory is registered; only instantiating it needs torch.
    assert "neural" in available_backends()


def test_unknown_backend_raises():
    with pytest.raises(BackendError):
        get_backend("does-not-exist")


def test_register_custom_backend():
    class SilentBackend(AcousticBackend):
        name = "silent"

        def render_segment(self, segment: Segment, sample_rate: int) -> np.ndarray:
            return np.zeros(max(1, round(segment.duration * sample_rate)), dtype=np.float32)

    register_backend("silent", SilentBackend)
    assert isinstance(get_backend("silent"), SilentBackend)

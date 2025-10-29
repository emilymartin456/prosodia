"""Acoustic backends: the pluggable stage that turns a plan into samples.

Backends are looked up by name so the facade and CLI can select one from config
without importing concrete classes. Register a custom backend with
:func:`register_backend`.
"""

from __future__ import annotations

from collections.abc import Callable

from prosodia.errors import BackendError
from prosodia.synthesis.backends.base import AcousticBackend
from prosodia.synthesis.backends.reference import FormantSynthBackend

__all__ = [
    "AcousticBackend",
    "FormantSynthBackend",
    "get_backend",
    "register_backend",
    "available_backends",
]

_REGISTRY: dict[str, Callable[..., AcousticBackend]] = {
    "reference": FormantSynthBackend,
}


def register_backend(name: str, factory: Callable[..., AcousticBackend]) -> None:
    """Register (or override) a backend factory under ``name``."""
    _REGISTRY[name] = factory


def get_backend(name: str = "reference", **kwargs: object) -> AcousticBackend:
    """Instantiate a registered backend by name."""
    if name not in _REGISTRY:
        raise BackendError(f"unknown backend: {name!r}; available: {available_backends()}")
    return _REGISTRY[name](**kwargs)


def available_backends() -> list[str]:
    return sorted(_REGISTRY)


def _register_optional_neural() -> None:
    """Expose the neural backend factory lazily (torch imported on use)."""
    from prosodia.synthesis.backends.neural import NeuralBackend

    _REGISTRY.setdefault("neural", NeuralBackend)


_register_optional_neural()

"""Exception hierarchy for prosodia.

All errors raised by the library derive from :class:`ProsodiaError`, so callers
can catch everything with a single ``except`` while still being able to narrow
down to a specific failure when they care.
"""

from __future__ import annotations


class ProsodiaError(Exception):
    """Base class for every error raised by prosodia."""


class ConfigError(ProsodiaError):
    """A configuration value is missing or inconsistent."""


class FrontendError(ProsodiaError):
    """The text frontend failed to process an input."""


class G2PError(FrontendError):
    """Grapheme-to-phoneme conversion failed for a token."""


class SynthesisError(ProsodiaError):
    """The synthesis stage failed to render audio."""


class BackendError(SynthesisError):
    """An acoustic backend raised while rendering."""


class BackendNotAvailable(BackendError):
    """A backend was requested but its dependencies are not installed."""


class AdapterError(ProsodiaError):
    """An LLM adapter failed to produce a usable result."""


class StreamingError(ProsodiaError):
    """The streaming engine hit an unrecoverable state."""

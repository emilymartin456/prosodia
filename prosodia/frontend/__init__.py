"""The text frontend: normalization, grapheme-to-phoneme and prosodic phrasing.

The public entry point is :class:`~prosodia.frontend.pipeline.TextFrontend`,
which turns a raw string into a fully analysed :class:`~prosodia.types.Utterance`.
"""

from __future__ import annotations

from prosodia.frontend.pipeline import TextFrontend

__all__ = ["TextFrontend"]

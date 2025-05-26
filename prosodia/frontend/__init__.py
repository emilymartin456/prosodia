"""The text frontend: normalization, grapheme-to-phoneme and prosodic phrasing.

The public entry point (added once the stages below exist) is
:class:`~prosodia.frontend.pipeline.TextFrontend`, which turns a raw string into
a fully analysed :class:`~prosodia.types.Utterance`.
"""

from __future__ import annotations

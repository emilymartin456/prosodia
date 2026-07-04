"""Synthesis: turning an analysed utterance into a renderable plan and audio.

The stage order is: :mod:`duration` and :mod:`contour` decide *how long* and
*what pitch* each phone gets, :mod:`plan` assembles those into a
:class:`~prosodia.synthesis.plan.SynthesisPlan`, and a backend under
:mod:`prosodia.synthesis.backends` renders it to samples.
"""

from __future__ import annotations

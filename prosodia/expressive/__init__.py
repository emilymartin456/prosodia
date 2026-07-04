"""Expressive control: emotions, style vectors and named presets.

The stages here sit between the frontend and synthesis: they turn a requested
emotion / style into the numeric :class:`~prosodia.types.ProsodyTargets` that the
synthesis plan honours.
"""

from __future__ import annotations

from prosodia.expressive.emotion import Emotion, get_emotion, list_emotions

__all__ = ["Emotion", "get_emotion", "list_emotions"]

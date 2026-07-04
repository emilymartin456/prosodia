"""Small logging helper so the whole package shares one configured logger."""

from __future__ import annotations

import logging
import os

_CONFIGURED = False


def get_logger(name: str = "prosodia") -> logging.Logger:
    """Return a package logger with a single stream handler attached once.

    The level honours the ``PROSODIA_LOG_LEVEL`` environment variable and
    defaults to ``INFO``. We disable propagation so importing prosodia does not
    add duplicate handlers to the root logger of a host application.
    """

    global _CONFIGURED
    logger = logging.getLogger(name)
    if not _CONFIGURED:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(name)s] %(levelname)s %(message)s")
        )
        root = logging.getLogger("prosodia")
        root.addHandler(handler)
        level = os.environ.get("PROSODIA_LOG_LEVEL", "INFO").upper()
        root.setLevel(getattr(logging, level, logging.INFO))
        root.propagate = False
        _CONFIGURED = True
    return logger

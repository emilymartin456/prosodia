"""Command-line entry point: ``prosodia <command> ...``.

Sub-command handlers import the heavy modules lazily so that ``prosodia
--version`` and ``prosodia --help`` stay fast.
"""

from __future__ import annotations

import argparse
import sys

from prosodia.version import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prosodia",
        description="情感 / 风格可控的表现力语音合成框架",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"prosodia {__version__}"
    )
    parser.add_subparsers(dest="command", metavar="<command>")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "func", None)
    if handler is None:
        parser.print_help()
        return 1
    result: int = handler(args)
    return result


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

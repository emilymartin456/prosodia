"""Command-line entry point: ``prosodia <command> ...``.

Sub-command handlers import the heavy modules lazily so that ``prosodia
--version`` and ``prosodia --help`` stay fast.
"""

from __future__ import annotations

import argparse
import sys

from prosodia.version import __version__


def _add_common_style(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-e", "--emotion", default="neutral", help="情感名称，如 happy / 高兴")
    parser.add_argument("--intensity", type=float, default=1.0, help="情感强度 0..3")
    parser.add_argument("--rate", type=float, default=1.0, help="语速倍率")
    parser.add_argument("--pitch", type=float, default=0.0, help="音高偏移（半音）")
    parser.add_argument("--sample-rate", type=int, default=22050)


def _cmd_say(args: argparse.Namespace) -> int:
    from prosodia import Config, ExpressiveTTS

    cfg = Config.from_dict({"audio": {"sample_rate": args.sample_rate}})
    tts = ExpressiveTTS(cfg)
    chunk = tts.to_wav(
        args.text,
        args.out,
        emotion=args.emotion,
        intensity=args.intensity,
        rate=args.rate,
        pitch_shift=args.pitch,
    )
    print(f"已写入 {args.out}（{chunk.duration:.2f} 秒，{chunk.sample_rate} Hz）")
    return 0


def _cmd_normalize(args: argparse.Namespace) -> int:
    from prosodia.frontend.normalize.pipeline import Normalizer
    from prosodia.types import Language

    print(Normalizer(Language(args.lang)).normalize(args.text))
    return 0


def _add_say(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("say", help="合成语音并写入 WAV")
    p.add_argument("text")
    p.add_argument("-o", "--out", default="out.wav")
    _add_common_style(p)
    p.set_defaults(func=_cmd_say)


def _add_normalize(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("normalize", help="文本规范化")
    p.add_argument("text")
    p.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    p.set_defaults(func=_cmd_normalize)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prosodia",
        description="情感 / 风格可控的表现力语音合成框架",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"prosodia {__version__}"
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    _add_say(sub)
    _add_normalize(sub)
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

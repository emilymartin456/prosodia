"""测量参考声学后端的实时率（RTF）。

对一组不同长度的文本各合成若干次，报告音频时长、墙钟耗时与 RTF。
```
python benchmarks/bench_rtf.py --repeat 20
```
"""

from __future__ import annotations

import argparse
import time

from prosodia import ExpressiveTTS
from prosodia.streaming.engine import StreamingEngine

TEXTS = {
    "short": "你好，世界。",
    "medium": "今天天气不错，我们出去走走吧，顺便买点东西。",
    "long": "语音合成的自然度，很大程度上取决于文本前端与韵律预测；" * 4,
}


def run(repeat: int) -> None:
    tts = ExpressiveTTS()
    engine = StreamingEngine(frontend=tts.frontend, backend=tts.backend, clock=time.perf_counter)
    print(f"{'case':<8}{'audio(s)':>10}{'wall(s)':>10}{'RTF':>8}")
    for name, text in TEXTS.items():
        audio_total = 0.0
        wall_total = 0.0
        for _ in range(repeat):
            _, stats = engine.run(text)
            audio_total += stats.audio_seconds
            wall_total += stats.wall_seconds
        rtf = wall_total / audio_total if audio_total else float("inf")
        print(f"{name:<8}{audio_total:>10.2f}{wall_total:>10.3f}{rtf:>8.4f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="prosodia RTF benchmark")
    parser.add_argument("--repeat", type=int, default=10)
    run(parser.parse_args().repeat)


if __name__ == "__main__":
    main()

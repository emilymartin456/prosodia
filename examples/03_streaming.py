"""流式合成：边合成边拿到音频块，并打印实时率与首包延迟。"""

from __future__ import annotations

from prosodia import ExpressiveTTS
from prosodia.streaming.sink import WavSink


def main() -> None:
    tts = ExpressiveTTS()
    text = "第一句话在这里。第二句稍微长一点，用来触发分块。第三句结束整段。"

    with WavSink("streamed.wav") as sink:
        for i, chunk in enumerate(tts.stream(text, emotion="calm")):
            sink.write(chunk)
            print(f"块 {i}: {chunk.duration:.2f}s")

    # 想要实时指标时，用 stream_to_wav：
    stats = tts.stream_to_wav(text, "streamed2.wav", emotion="calm")
    print(stats.summary())


if __name__ == "__main__":
    main()

"""最简示例：把一句话合成成 WAV 文件。"""

from __future__ import annotations

from prosodia import ExpressiveTTS


def main() -> None:
    tts = ExpressiveTTS()
    text = "你好，世界！很高兴认识你。"
    audio = tts.to_wav(text, "basic.wav", emotion="happy")
    print(f"已写入 basic.wav：{audio.duration:.2f} 秒，{audio.sample_rate} Hz")


if __name__ == "__main__":
    main()

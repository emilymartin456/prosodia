"""遍历内置情感，为每种情感合成同一句话。"""

from __future__ import annotations

from prosodia import ExpressiveTTS, list_emotions


def main() -> None:
    tts = ExpressiveTTS()
    text = "今天的消息，你听说了吗？"
    for emotion in list_emotions():
        audio = tts.to_wav(text, f"emotion_{emotion}.wav", emotion=emotion, intensity=1.2)
        print(f"{emotion:<10} -> emotion_{emotion}.wav  ({audio.duration:.2f}s)")


if __name__ == "__main__":
    main()

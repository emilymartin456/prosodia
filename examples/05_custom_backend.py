"""自定义声学后端：实现 AcousticBackend 并注册，然后照常合成。

这里的后端把每个音段渲染成一段纯正弦（按基频），只是演示扩展点——
真实场景可以在这里接入训练好的声码器。
"""

from __future__ import annotations

import numpy as np

from prosodia import Config, ExpressiveTTS
from prosodia.synthesis.backends import available_backends, register_backend
from prosodia.synthesis.backends.base import AcousticBackend
from prosodia.synthesis.plan import Segment


class SineBackend(AcousticBackend):
    name = "sine"

    def render_segment(self, segment: Segment, sample_rate: int) -> np.ndarray:
        n = max(1, round(segment.duration * sample_rate))
        if segment.is_silence or segment.f0 is None:
            return np.zeros(n, dtype=np.float32)
        f0 = np.interp(
            np.linspace(0, len(segment.f0) - 1, n),
            np.arange(len(segment.f0)),
            segment.f0,
        )
        phase = 2 * np.pi * np.cumsum(f0) / sample_rate
        return (0.3 * np.sin(phase)).astype(np.float32)


def main() -> None:
    register_backend("sine", SineBackend)
    print("可用后端:", available_backends())

    tts = ExpressiveTTS(Config(), backend=SineBackend())
    audio = tts.to_wav("你好世界", "sine.wav")
    print(f"用自定义后端写出 sine.wav：{audio.duration:.2f}s")


if __name__ == "__main__":
    main()

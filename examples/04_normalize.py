"""文本规范化：把书写形式改写成朗读形式。"""

from __future__ import annotations

from prosodia.frontend.normalize.pipeline import Normalizer
from prosodia.types import Language

SAMPLES = [
    "2026年7月5日 上午9:30 开会",
    "打八折，只要 ¥199",
    "气温 37℃，湿度 60%",
    "本店距地铁站 1.5km",
]


def main() -> None:
    zh = Normalizer(Language.ZH)
    for text in SAMPLES:
        print(f"{text}\n  -> {zh.normalize(text)}\n")

    en = Normalizer(Language.EN)
    print("It costs $5.\n  ->", en.normalize("It costs $5."))


if __name__ == "__main__":
    main()

"""prosodia — 情感 / 风格可控的表现力语音合成框架。

顶层暴露最常用的入口 :class:`ExpressiveTTS` 与风格控制类型，子模块按需导入。
"""

from prosodia.config import Config
from prosodia.expressive import StyleControl, get_emotion, list_emotions
from prosodia.pipeline import ExpressiveTTS
from prosodia.types import Language
from prosodia.version import __version__

__all__ = [
    "__version__",
    "ExpressiveTTS",
    "Config",
    "StyleControl",
    "Language",
    "get_emotion",
    "list_emotions",
]

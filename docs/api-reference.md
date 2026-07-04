# API 参考

只列稳定的公开接口。内部工具可能随版本变化。

## 顶层 `prosodia`

```python
from prosodia import (
    ExpressiveTTS, Config, StyleControl, Language,
    get_emotion, list_emotions, __version__,
)
```

### `ExpressiveTTS(config=None, backend=None, adapter=None)`

| 方法 | 说明 |
|------|------|
| `say(text, emotion=None, *, style=None, rate=None, pitch_shift=None, energy=None, intensity=None) -> AudioChunk` | 一次合成 |
| `to_wav(text, path, **kwargs) -> AudioChunk` | 合成并写 WAV |
| `stream(text, ...) -> Iterator[AudioChunk]` | 流式产出音频块 |
| `stream_to_wav(text, path, **kwargs) -> StreamStats` | 流式写 WAV，返回指标 |
| `analyze(text) -> Utterance` | 只跑前端 |

## 文本前端

```python
from prosodia.frontend import TextFrontend
TextFrontend(language=Language.AUTO, normalize=True, phraser=None).process(text) -> Utterance

from prosodia.frontend.normalize.pipeline import Normalizer, detect_language
from prosodia.frontend.g2p import chinese_g2p, english_g2p, to_pinyin
from prosodia.frontend.g2p.sandhi import apply_sandhi
from prosodia.frontend.phrasing import PhraseBreaker, RuleBasedPhraser
```

## 表现力

```python
from prosodia.expressive import StyleControl, StyleVector, get_emotion, list_emotions
from prosodia.expressive.presets import get_preset, list_presets

StyleControl(emotion="neutral", intensity=1.0, rate=1.0,
             pitch_shift=0.0, energy=1.0, pause_scale=1.0, base_f0=200.0)
StyleControl(...).to_targets() -> ProsodyTargets
```

## 合成

```python
from prosodia.synthesis.plan import build_plan, SynthesisPlan, Segment
from prosodia.synthesis.f0 import f0_for_tone
from prosodia.synthesis.duration import phone_duration, syllable_duration
from prosodia.synthesis.backends import (
    AcousticBackend, FormantSynthBackend,
    get_backend, register_backend, available_backends,
)
```

自定义后端只需实现一个方法：

```python
class MyBackend(AcousticBackend):
    name = "my"
    def render_segment(self, segment: Segment, sample_rate: int) -> np.ndarray: ...
```

## 语言模型适配器

```python
from prosodia.llm import LLMAdapter, ProsodyPrediction, RuleBasedAdapter
from prosodia.llm.openai_compat import OpenAICompatibleAdapter
from prosodia.llm.cache import CachingAdapter

adapter.normalize(text, language) -> str
adapter.predict_prosody(text, language) -> ProsodyPrediction
```

## 音频与流式

```python
from prosodia.audio.chunk import AudioChunk, concat
from prosodia.audio.wav import read_wav, write_wav
from prosodia.audio.resample import resample
from prosodia.streaming.engine import StreamingEngine
from prosodia.streaming.metrics import StreamStats, real_time_factor
from prosodia.streaming.chunker import chunk_text
from prosodia.streaming.sink import WavSink, CallbackSink, drain
```

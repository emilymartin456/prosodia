# 使用指南

## 安装

```bash
pip install prosodia            # 核心
pip install "prosodia[llm]"     # + openai
pip install "prosodia[neural]"  # + torch
pip install "prosodia[dev]"     # 开发依赖（pytest/ruff/mypy）
```

## Python API

### 一次合成

```python
from prosodia import ExpressiveTTS

tts = ExpressiveTTS()
audio = tts.say("你好，世界。", emotion="happy", rate=1.1)
tts.to_wav("你好，世界。", "out.wav", emotion="sad", intensity=1.5)
```

`say` 的可选参数：

| 参数 | 含义 |
|------|------|
| `emotion`     | 情感名称或中文别名（`happy` / `高兴`） |
| `intensity`   | 情感强度，`0..3`（`0` 退化为中性） |
| `rate`        | 语速倍率（`>1` 更快） |
| `pitch_shift` | 音高偏移（半音） |
| `energy`      | 能量（音量）倍率 |
| `style`       | 直接传入 `StyleControl`，覆盖以上 |

### 用配置

```python
from prosodia import Config, ExpressiveTTS

cfg = Config.from_dict({
    "audio": {"sample_rate": 16000},
    "frontend": {"language": "zh"},
    "expressive": {"emotion": "calm", "intensity": 0.8},
})
tts = ExpressiveTTS(cfg)
```

也支持 `Config.from_yaml("config.yaml")`（需 `prosodia[yaml]`）。

### 只看前端

```python
utt = tts.analyze("2026年7月5日，气温37℃。")
print(utt.normalized)                     # 规范化文本
for w in utt.words:
    print(w.text, [s.text for s in w.syllables], w.break_after.name)
```

## 命令行

```bash
prosodia say "你好世界" -o hello.wav -e 高兴 --rate 1.1
prosodia stream "第一句。第二句。" -o stream.wav
prosodia normalize "只要 ¥199，2026年7月5日截止"
prosodia phonemize "你好世界"
prosodia prosody "你好，世界。"
prosodia emotions
prosodia bench --repeat 5
```

## 接入语言模型

默认使用离线规则适配器。要接入 OpenAI 兼容端点：

```python
from prosodia import ExpressiveTTS
from prosodia.llm.openai_compat import OpenAICompatibleAdapter
from prosodia.llm.cache import CachingAdapter

adapter = OpenAICompatibleAdapter(model="gpt-4o-mini")  # 读取标准 OPENAI_* 环境变量
adapter = CachingAdapter(adapter, ".prosodia-cache")     # 加磁盘缓存，保证可复现
tts = ExpressiveTTS(adapter=adapter)
```

单元测试里可以注入一个假的 `chat_fn`，完全不联网。

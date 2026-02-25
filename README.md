# prosodia

> 情感 / 风格可控的**表现力语音合成框架**：以语言模型驱动文本前端（规范化 + 韵律预测），
> 内置**流式与实时**推理，纯 Python、离线优先、可复现。

[![CI](https://github.com/emilymartin456/prosodia/actions/workflows/ci.yml/badge.svg)](https://github.com/emilymartin456/prosodia/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

`prosodia` 把一段中文/英文文本，经过**文本前端 → 表现力控制 → 声学后端 → 流式输出**四个阶段，
合成为带情感与风格的语音。它把「难点」放在**前端与韵律**上：数字/日期/货币的规范化、拼音注音与
变调、韵律短语切分、情感到韵律参数的映射，以及一个**可插拔的声学后端**接口。框架自带一个纯 NumPy 的
**参考声码器**（共振峰源-滤波合成），因此开箱即可离线跑通、出声、可测试；生产环境可把神经声学模型
接到同一个 `AcousticBackend` 接口上。

## 特性

- 🈶 **中文文本前端**：数字 / 日期 / 时间 / 金额 / 单位 / 百分号规范化；`pypinyin` 注音（TONE3）；
  三声连读、「不 / 一」变调。
- 🗣️ **韵律预测**：基于规则的韵律短语切分（标点 + 音节预算），可插拔的 `PhraseBreaker` 接口。
- 🤖 **接入语言模型**：统一的 `LLMAdapter` 接口做文本规范化与韵律预测；默认是**离线规则适配器**，
  也可切换到 OpenAI 兼容端点；带磁盘缓存保证可复现。
- 🎭 **情感 / 风格可控**：内置 8 种情感（含中文别名）与命名风格预设，情感强度、语速、音高、
  能量、停顿均可连续调节。
- ⚡ **流式与实时**：按句/短语切块的流式引擎，边合成边出块，附带实时率（RTF）与首包延迟指标。
- 🔌 **可插拔后端**：`AcousticBackend` 注册表；自带参考共振峰合成器，预留神经后端接入点。
- 🧰 **CLI**：`say` / `stream` / `normalize` / `phonemize` / `prosody` / `emotions` / `bench`。

## 安装

```bash
pip install prosodia            # 核心：numpy + pypinyin，纯 Python
pip install "prosodia[llm]"     # 额外：openai（接入语言模型）
pip install "prosodia[neural]"  # 额外：torch（神经声学后端）
```

## 快速开始

```python
from prosodia import ExpressiveTTS

tts = ExpressiveTTS()

# 一次合成
audio = tts.say("你好，世界！今天是 2026 年 7 月 5 日。", emotion="happy")
audio  # AudioChunk(samples=float32, sample_rate=22050)

# 直接写 WAV
tts.to_wav("语速更快，语气平静。", "out.wav", emotion="calm", rate=1.2)

# 流式合成，拿到实时指标
stats = tts.stream_to_wav("第一句。第二句。第三句。", "stream.wav")
print(stats.summary())   # 3 chunks, audio=..., RTF=...
```

命令行：

```bash
prosodia say "你好世界" -o hello.wav --emotion 高兴 --rate 1.1
prosodia normalize "打八折，只要 ¥199，2026年7月5日截止"
prosodia phonemize "你好世界"          # ni3 hao3 shi4 jie4
prosodia prosody "你好，世界。"          # 打印规范化 + 每词的注音与韵律边界
prosodia emotions                      # 列出情感及其韵律参数
prosodia bench                         # 测量 RTF
```

## 管线一览

```
      文本
       │
       ▼
┌──────────────┐   规范化 → 注音(变调) → 韵律短语
│  文本前端     │   frontend/  (可由 LLMAdapter 接管)
└──────┬───────┘
       ▼           情感 + 强度 + 手动覆盖 → ProsodyTargets
┌──────────────┐
│  表现力控制   │   expressive/
└──────┬───────┘
       ▼           时长模型 + 基频曲线 → SynthesisPlan
┌──────────────┐
│   合成规划     │  synthesis/
└──────┬───────┘
       ▼           AcousticBackend（参考共振峰 / 神经）
┌──────────────┐
│  声学后端     │   synthesis/backends/
└──────┬───────┘
       ▼           分块流式 + RTF/延迟
┌──────────────┐
│  流式引擎     │   streaming/
└──────┬───────┘
       ▼
   音频 / WAV / 回调
```

## 文档

- [架构总览](docs/architecture.md)
- [使用指南](docs/usage.md)
- [设计笔记：韵律与表现力控制](docs/design-notes.md)
- [API 参考](docs/api-reference.md)
- [流式与实时推理](docs/streaming.md)
- 更多可运行示例见 [`examples/`](examples/)。

## 说明

自带的参考声码器面向**可复现与可测试**，并非追求音质的神经模型；它让整条管线离线可跑、
出声、可断言。要接入高音质后端，实现 `AcousticBackend` 并注册即可。

## 许可证

[MIT](LICENSE) © 2026 Jiang Que

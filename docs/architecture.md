# 架构总览

`prosodia` 是一条四阶段的合成管线，每个阶段只依赖上一阶段的数据结构，边界清晰、可替换。

```
文本 ─▶ 文本前端 ─▶ 表现力控制 ─▶ 合成规划 ─▶ 声学后端 ─▶ 流式引擎 ─▶ 音频
        frontend/     expressive/    synthesis/    backends/     streaming/
```

## 数据流与核心类型

所有阶段共享 `prosodia/types.py` 里的轻量类型（`dataclass` + `Enum`，不依赖 numpy），
因此纯文本处理无需引入音频栈：

- `Language`：`zh` / `en` / `auto`。
- `Phone` / `Syllable` / `Word` / `Utterance`：前端产出的层级结构。
- `BreakLevel`：`NONE / WORD / PHRASE / SENTENCE`，每级对应一个停顿时长。
- `ProsodyTargets`：表现力控制的数值结果（语速、音高偏移、音高范围、能量、停顿缩放、基频）。

## 各阶段职责

### 文本前端 `frontend/`
- `normalize/`：数字（中/英）、日期时间、货币与单位、百分号/千分号规范化。
- `g2p/`：`pypinyin` 注音（TONE3）+ 三声/「不·一」变调；英文走近似字母到音的兜底。
- `phrasing.py`：韵律短语切分（`PhraseBreaker` 接口 + 规则实现）。
- `pipeline.py`：把上面拼装成 `Utterance`。

### 表现力控制 `expressive/`
- `emotion.py`：情感目录（含中文别名），每种情感是一组相对中性的韵律增量。
- `style.py`：`StyleVector`（可混合/叠加）与 `StyleControl`（情感 + 强度 + 手动覆盖 → `ProsodyTargets`）。
- `presets.py`：命名风格预设（新闻播报、讲故事、客服……）。

### 合成规划 `synthesis/`
- `duration.py`：确定性时长模型（元音/辅音基准时长，按语速缩放）。
- `f0.py`：由声调形状生成基频曲线。
- `plan.py`：把 `Utterance` + `StyleControl` 展开成 `SynthesisPlan`（逐音段 + 断句静音）。

### 声学后端 `synthesis/backends/`
- `base.py`：`AcousticBackend` 抽象类，只需实现 `render_segment`。
- `reference.py`：纯 NumPy 共振峰源-滤波参考合成器（确定性、离线）。
- `neural.py`：神经后端接入点（延迟导入 torch）。
- 通过注册表 `get_backend` / `register_backend` 按名选择。

### 流式引擎 `streaming/`
- `chunker.py`：按句/短语切块，控制单块字数。
- `engine.py`：逐块合成、即时产出，记录 `StreamStats`。
- `metrics.py`：实时率（RTF）与首包延迟。
- `sink.py`：`WavSink` / `CallbackSink`。

## 设计取舍

- **纯 Python 核心 + 可选重依赖**：核心只需 `numpy` + `pypinyin`；`torch`、`openai` 都是可选 extra。
  这让 CI 快、可复现，也符合「离线优先」。
- **接口先行**：`AcousticBackend`、`LLMAdapter`、`PhraseBreaker` 都是窄接口，规则实现与模型实现可互换。
- **前端做重活**：真正影响自然度的是规范化与韵律，框架把工程重心放在这里，声学后端可插拔。

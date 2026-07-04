# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 与
[语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [0.1.0] - 2026-07-05

### Added
- 文本前端：中/英数字、日期时间、货币与单位、百分号/千分号规范化。
- `pypinyin` 注音（TONE3），三声连读与「不 / 一」变调。
- 规则韵律短语切分，可插拔的 `PhraseBreaker` 接口。
- 情感目录（8 种，含中文别名）与命名风格预设。
- `StyleControl` / `StyleVector`：情感 + 强度 + 手动覆盖 → `ProsodyTargets`。
- 确定性时长模型与声调基频曲线。
- 纯 NumPy 共振峰参考声学后端，及后端注册表。
- 神经后端接入点（延迟导入 torch）。
- `LLMAdapter` 接口：离线规则适配器、OpenAI 兼容适配器、磁盘缓存适配器。
- 流式引擎：按句/短语切块、实时率与首包延迟指标、`WavSink` / `CallbackSink`。
- 命令行：`say` / `stream` / `normalize` / `phonemize` / `prosody` / `emotions` / `bench`。

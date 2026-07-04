# 示例

这些脚本都可以直接运行，覆盖框架的主要用法。除 `05_custom_backend.py` 外都只依赖核心安装
（`numpy` + `pypinyin`），完全离线。

```bash
python examples/01_basic_say.py
python examples/02_emotion_control.py
python examples/03_streaming.py
python examples/04_normalize.py
python examples/05_custom_backend.py
```

| 脚本 | 演示内容 |
|------|----------|
| `01_basic_say.py`      | 最简合成，写出一个 WAV |
| `02_emotion_control.py`| 遍历内置情感，每种写一个 WAV |
| `03_streaming.py`      | 流式合成并打印实时率（RTF）与首包延迟 |
| `04_normalize.py`      | 文本规范化：数字 / 日期 / 金额 / 单位 |
| `05_custom_backend.py` | 实现并注册一个自定义声学后端 |

# 贡献指南

欢迎提 issue 与 PR。下面是本地开发的最短路径。

## 环境

```bash
git clone https://github.com/emilymartin456/prosodia.git
cd prosodia
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## 提交前自检

CI 会跑这三项，请在本地先跑通：

```bash
ruff check .
ruff format --check .
mypy
pytest -q
```

## 约定

- **代码风格**：`ruff` 负责 lint 与 format，行宽 100。
- **类型**：公开函数尽量带类型注解，`mypy` 需通过。
- **测试**：新功能要有对应测试，测试文件与模块一一对应（`tests/test_<module>.py`）。
- **提交信息**：推荐 Conventional Commits（`feat:` / `fix:` / `docs:` / `refactor:` / `chore:`），
  但不强制。
- **依赖**：核心只允许 `numpy` 与 `pypinyin`；其余走可选 extra。请不要给核心加重依赖。

## 加一个声学后端

实现 `AcousticBackend.render_segment`，然后 `register_backend("name", Factory)` 即可，
参考 `examples/05_custom_backend.py`。

## 加一个语言模型适配器

实现 `LLMAdapter` 的 `normalize` 与 `predict_prosody`。网络调用请隔离在可注入的回调后面，
以便离线测试（见 `OpenAICompatibleAdapter` 的 `chat_fn`）。

---
name: pyright-lsp-tool
description: On-demand Pyright LSP query tool (references) without running a full editor LSP.
---

# pyright-lsp-tool

一个“可自由启停”的 Pyright LSP 小工具：需要查语义级引用时临时启动 `pyright-langserver`（或保持一段时间常驻），查询完成后退出即可。

本 skill **独立于其它 skill**，不读取/依赖 `ai-team-workflow` 或其它配置文件；其它 skill 也不应引用它。

## 依赖

- `pyright`（提供 `pyright-langserver`）
  - 推荐装到你的项目 venv：`pip install pyright`
- `node`（pyright 运行时需要）

## 用法

进入目标仓库根目录后运行（默认会用 `git rev-parse --show-toplevel` 作为 project root）：

- 交互模式（推荐：一次启动，多次查询；退出即停）
  - `python3 .codex/skills/pyright-lsp-tool/scripts/pyright_lsp_tool.py repl`
  - 在交互提示符里：
    - `refs src/pages/common/login_page.py:62:9`
  - 退出：`exit`

- 单次查询（每次都会启动一次 server，冷启动会慢一些）
  - `python3 .codex/skills/pyright-lsp-tool/scripts/pyright_lsp_tool.py refs src/pages/common/login_page.py:62:9`

可选参数：
- `--root <path>`：指定 project root（默认：git toplevel 或 cwd）
- `--venv <venv_dir>`：指定 venv（用于定位 `pyright-langserver`）


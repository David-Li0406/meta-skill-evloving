---
name: coding-agent-runner
description: 在仓库内通过脚本调度多个 coding agent（codex、opencode、claude code）执行任务。用户提到运行 codex/opencode/claude、委派任务给 coding agent、希望自动改代码并跑命令或测试时使用。
version: 1.0.0
allowed-tools: ["Bash", "Read", "Grep", "Glob"]
---

# Coding Agent Runner

这个 Skill 用于把用户需求转换成可复用的 CLI 调用，通过一个统一脚本在同一仓库内调度多个 coding agent：`codex`、`opencode`、`claude`（Claude Code CLI），并在执行后做基本校验。

## Quick Start

1. 确认本机 CLI 可用：

```bash
codex --version
claude --version
```

1. 用统一脚本运行（建议在仓库根目录执行）：

```bash
python3 .claude/skills/coding-agent-runner/scripts/invoke_coding_agent.py --agent codex --prompt "分析当前仓库并给出修复方案" --model gpt-4o --dry-run
```

1. 执行一次真实运行（会调用对应 agent CLI）：

```bash
python3 .claude/skills/coding-agent-runner/scripts/invoke_coding_agent.py --agent claude --prompt "检查当前目录下的未提交更改并总结"
```

## Instructions

### 1) Preflight

1. 确认当前工作目录是目标仓库。
2. 确认目标 agent 的 CLI 存在且可执行：`codex` / `opencode` / `claude`。
3. 确认认证变量已配置（不要打印密钥本体）：

```bash
test -n "${OPENAI_API_KEY:-}" && echo "OPENAI_API_KEY is set" || echo "OPENAI_API_KEY is not set"
test -n "${ANTHROPIC_API_KEY:-}" && echo "ANTHROPIC_API_KEY is set" || echo "ANTHROPIC_API_KEY is not set"
```

如果用户要使用 OpenAI API key 登录 `codex`，按官方方式：

```bash
printenv OPENAI_API_KEY | codex login --with-api-key
```

### 2) 把用户需求改写成可执行 Prompt

Prompt 建议包含：

- Goal：要实现/修复什么。
- Scope：哪些目录/文件允许改。
- Constraints：不修改生成产物（例如 `bin/` shim）、不新增依赖（除非用户明确要求）、不打印或记录任何 secrets。
- Verification：要跑哪些命令（lint/typecheck/tests/build）以及成功标准。

尽量短、明确、命令式；必要时把路径写清楚。

### 3) 选择合适的 Agent 与模式

- `codex`: 用于快速执行与自动修改，可选 `--full-auto` 与 `--json`。
- `claude` (Claude Code CLI): 用 `claude -p "..."` 做单次命令式运行，可选 `--output-format json`（脚本已自动处理）。
- `opencode`: 用 `opencode run "..."` 做非交互任务（依赖本机安装与配置）。

### 4) 通过统一脚本执行

统一使用 `.claude/skills/coding-agent-runner/scripts/invoke_coding_agent.py`，把 agent、工作目录、Prompt 和额外参数收敛到一个入口。

支持指定模型：使用 `--model` 或 `-m` 参数。

示例：

```bash
python3 .claude/skills/coding-agent-runner/scripts/invoke_coding_agent.py --agent codex --prompt "解释 scripts/pwsh 下的安装流程" --dry-run
```

```bash
# 指定模型为 gpt-4o
python3 .claude/skills/coding-agent-runner/scripts/invoke_coding_agent.py --agent codex --prompt "修复 failing tests" --model gpt-5.2 --full-auto --dry-run
```

### 5) 结束后校验与交付

执行完成后：

1. 复查变更：

```bash
git diff
```

1. 跑用户要求的验证命令（或仓库标准的 lint/typecheck/tests/build）。
2. 汇总：
   - Files changed
   - Commands run + 结果
   - 剩余限制与后续动作

## Notes

- 不要输出 `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` 或任何 credentials。
- 如果 agent 改动超出 Scope，先回滚再用更严格的 Prompt 重跑。

## Reference

### Supported Agents & Options

- **codex** (Internal coding agent)
  - `exec`: Execute a task.
  - `--model <MODEL>`: Specify model (e.g., gpt-4o).
  - `--full-auto`: Run without confirmation.
  - `-C <path>`: Specify context directory.
  - `--json`: Output JSON format.

- **claude** (Claude Code CLI)
  - `-p <prompt>`: Provide prompt.
  - `--model <model>`: Model for the current session (e.g., claude-3-5-sonnet).
  - `--setting-sources user,project,local`: Load settings from multiple sources.
  - `--output-format json`: Output JSON format.
  - `--verbose`: Enable verbose output.

- **opencode** (Open source runner)
  - `run <prompt>`: Run a task.
  - `--model <provider/model>`: Model to use (e.g., openai/gpt-4o).

For more detailed documentation and cheat sheets, refer to:

- [Claude Code Cheatsheet](../../docs/CLAUDE_CODE_CHEATSHEET.md)

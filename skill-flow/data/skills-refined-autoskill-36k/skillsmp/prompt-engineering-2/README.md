# prompt-engineering

通用提示词工程技能，用于设计、改写、评审和标准化提示词，覆盖清晰直接、结构化、few-shot、链式提示、长上下文与评估迭代等场景。

## 内容结构
```
.
├── SKILL.md
└── references/
    ├── overview.md
    ├── be-clear-and-direct.md
    ├── multishot-prompting.md
    ├── chain-of-thought.md
    ├── use-xml-tags.md
    ├── system-prompts.md
    ├── prefill-response.md
    ├── chain-prompts.md
    ├── long-context-tips.md
    ├── extended-thinking-tips.md
    ├── prompt-templates-and-variables.md
    ├── prompt-generator.md
    ├── prompt-improver.md
    ├── claude-4-best-practices.md
    └── openai-prompt-engineering.md
```

## 使用方式
- 触发式使用：当任务涉及提示词设计/改写/评审/模板化/迭代时直接调用该技能。
- 需要深入细节时，按 SKILL.md 中的导航加载对应 references 文件。

## 快速安装
支持的 Agent 与安装位置：

| Agent | Flag | Install Location |
| --- | --- | --- |
| Claude Code | --agent claude | ~/.claude/skills/ |
| Cursor | --agent cursor | .cursor/skills/ |
| Codex | --agent codex | ~/.codex/skills/ |
| Amp | --agent amp | ~/.amp/skills/ |
| VS Code / Copilot | --agent vscode | .github/skills/ |
| Goose | --agent goose | ~/.config/goose/skills/ |
| OpenCode | --agent opencode | ~/.opencode/skill/ |
| Letta | --agent letta | ~/.letta/skills/ |
| Portable | --agent project | .skills/ |

示例（Codex）：
```bash
npx -y ai-agent-skills install fancyboi999/prompt-engineering --agent codex
```

安装到所有支持的 Agent（默认行为）：
```bash
npx -y ai-agent-skills install fancyboi999/prompt-engineering
```

便携安装（项目内目录，适配任意 Agent）：
```bash
npx -y ai-agent-skills install fancyboi999/prompt-engineering --agent project
```

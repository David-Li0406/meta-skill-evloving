---
name: codeagent
description: Use this skill when you need to execute codeagent-wrapper commands for multi-backend AI code tasks, supporting Codex, Claude, and Gemini backends with file references and structured output.
---

# Codeagent Wrapper Integration

## Overview

Execute codeagent-wrapper commands with pluggable AI backends (Codex, Claude, Gemini). Supports file references via `@` syntax, parallel task execution with backend selection, and configurable security controls.

## When to Use

- Complex code analysis requiring deep understanding
- Large-scale refactoring across multiple files
- Automated code generation with backend selection

## Usage

**HEREDOC syntax** (recommended):
```bash
codeagent-wrapper --backend codex - [working_dir] <<'EOF'
<task content here>
EOF
```

**With backend selection**:
```bash
codeagent-wrapper --backend claude - [working_dir] <<'EOF'
<task content here>
EOF
```

**Simple tasks**:
```bash
codeagent-wrapper --backend codex "simple task" [working_dir]
codeagent-wrapper --backend gemini "simple task" [working_dir]
```

## Backends

| Backend | Command            | Description            | Best For                             |
| ------- | ------------------ | ---------------------- | ------------------------------------ |
| codex   | `--backend codex`  | OpenAI Codex (default) | Code analysis, complex development   |
| claude  | `--backend claude` | Anthropic Claude       | Simple tasks, documentation, prompts |
| gemini  | `--backend gemini` | Google Gemini          | UI/UX prototyping                    |

### Backend Selection Guide

**Codex** (default):
- Deep code understanding and complex logic implementation
- Large-scale refactoring with precise dependency tracking
- Algorithm optimization and performance tuning
- Example: "Analyze the call graph of @src/core and refactor the module dependency structure"

**Claude**:
- Quick feature implementation with clear requirements
- Technical documentation, API specs, README generation
- Professional prompt engineering (e.g., product requirements, design specs)
- Example: "Generate a comprehensive README for @package.json with installation, usage, and API docs"

**Gemini**:
- UI component scaffolding and layout prototyping
- Design system implementation with style consistency
- Interactive element generation with accessibility support
- Example: "Create a responsive dashboard layout with sidebar navigation and data visualization cards"

**Backend Switching**:
- Start with Codex for analysis, switch to Claude for documentation, then Gemini for UI implementation
- Use per-task backend selection in parallel mode to optimize for each task's strengths
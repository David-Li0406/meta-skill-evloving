---
name: codex
description: Use this skill when you need to delegate complex code tasks to Codex AI for code analysis, refactoring, and automated code changes with structured output.
---

# Codex CLI Integration

## Overview

Execute Codex CLI commands and parse structured JSON responses. Supports file references via `@` syntax, multiple models, and sandbox controls.

## When to Use

- Complex code analysis requiring deep understanding
- Large-scale refactoring across multiple files
- Automated code generation with safety controls

## Fallback Policy

Codex is the **primary execution method** for all code edits and tests. Direct execution is only permitted when:

1. Codex is unavailable (service down, network issues)
2. Codex fails **twice consecutively** on the same task

When falling back to direct execution:
- Log `CODEX_FALLBACK` with the reason
- Retry Codex on the next task (don't permanently switch)
- Document the fallback in the final summary

## Usage

**Mandatory**: Run every automated invocation through the Bash tool in the foreground with **HEREDOC syntax** to avoid shell quoting issues, keeping the `timeout` parameter fixed at `7200000` milliseconds (do not change it or use any other entry point).

```bash
codex-wrapper - [working_dir] <<'EOF'
<task content here>
EOF
```

**Why HEREDOC?** Tasks often contain code blocks, nested quotes, shell metacharacters (`$`, `` ` ``, `\`), and multiline text. HEREDOC (Here Document) syntax passes these safely without shell interpretation, eliminating quote-escaping nightmares.

**Foreground only (no background/BashOutput)**: Never set `background: true`, never accept Claude's "Running in the background" mode, and avoid `BashOutput` streaming loops. Keep a single foreground Bash call per Codex task; if work might be long, split it into smaller foreground runs instead of offloading to background execution.

**Simple tasks** (backward compatibility):
For simple single-line tasks without special characters, you can still use direct quoting:
```bash
codex-wrapper "simple task here" [working_dir]
```

**Resume a session with HEREDOC:**
```bash
codex-wrapper resume <session_id> - [working_dir] <<'EOF'
<task content>
EOF
```

**Cross-platform notes:**
- **Bash/Zsh**: Use `<<'EOF'` (single quotes prevent variable expansion)
- **PowerShell 5.1+**: Use `@'` and `'@` (here-string syntax)
  ```powershell
  codex-wrapper - @'
  task content
  '@
  ```

## Environment Variables

- *
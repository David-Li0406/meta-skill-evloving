---
name: codex
description: Use this skill when the user asks to run Codex CLI (codex exec, codex resume) or references OpenAI Codex for code analysis, refactoring, or automated editing.
---

# Codex Skill Guide

## Running a Task
1. Default to `gpt-5.2` model. Ask the user (via `AskUserQuestion`) which reasoning effort to use (`xhigh`, `high`, `medium`, or `low`). The user can override the model if needed.
2. Select the sandbox mode required for the task; default to `--sandbox read-only` unless edits or network access are necessary.
3. Assemble the command with the appropriate options:
   - `-m, --model <MODEL>`
   - `--config model_reasoning_effort="<high|medium|low>"`
   - `--sandbox <read-only|workspace-write|danger-full-access>`
   - `--full-auto`
   - `-C, --cd <DIR>`
   - `--skip-git-repo-check`
4. Always use `--skip-git-repo-check`.
5. When continuing a previous session, use `codex exec --skip-git-repo-check resume --last` via stdin. When resuming, don't use any configuration flags unless explicitly requested by the user. Resume syntax: `echo "your prompt here" | codex exec --skip-git-repo-check resume --last 2>/dev/null`. All flags must be inserted between exec and resume.
6. **IMPORTANT**: By default, append `2>/dev/null` to all `codex exec` commands to suppress thinking tokens (stderr). Only show stderr if the user explicitly requests to see thinking tokens or if debugging is needed.
7. Run the command, capture stdout/stderr (filtered as appropriate), and summarize the outcome for the user.
8. **After Codex completes**, inform the user: "You can resume this Codex session at any time by saying 'codex resume' or asking me to continue with additional analysis or changes."

### Quick Reference
| Use case | Sandbox mode | Key flags |
| --- | --- | --- |
| Read-only review or analysis | `read-only` | `--sandbox read-only 2>/dev/null` |
| Apply local edits | `workspace-write` | `--sandbox workspace-write --full-auto 2>/dev/null` |
| Permit network or broad access | `danger-full-access` | `--sandbox danger-full-access --full-auto 2>/dev/null` |
| Resume recent session | Inherited from original | `echo "prompt" \| codex exec --skip-git-repo-check resume --last 2>/dev/null` (no flags allowed) |
| Run from another directory | Match task needs | `-C <DIR>` plus other flags `2>/dev/null` |
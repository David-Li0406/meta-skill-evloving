---
name: codex-cli
description: Use this skill when you need to run the Codex CLI for code analysis, refactoring, or automated editing tasks.
---

# Codex Skill Guide

Orchestrate OpenAI Codex CLI for various coding tasks.

## Running a Task
1. Ask the user (via `AskUserQuestion`) which model to run (`gpt-5.2-codex` or `gpt-5.2`) AND which reasoning effort to use (`xhigh`, `high`, `medium`, or `low`) in a **single prompt with two questions**.
2. Select the sandbox mode required for the task; default to `--sandbox read-only` unless edits or network access are necessary.
3. Assemble the command with the appropriate options:
   - `-m, --model <MODEL>`
   - `--config model_reasoning_effort="<xhigh|high|medium|low>"`
   - `--sandbox <read-only|workspace-write|danger-full-access>`
   - `--full-auto`
   - `-C, --cd <DIR>`
   - `--skip-git-repo-check`
4. Always use `--skip-git-repo-check`.
5. When continuing a previous session, use `codex exec --skip-git-repo-check resume --last` via stdin. Resume syntax: `echo "your prompt here" | codex exec --skip-git-repo-check resume --last 2>/dev/null`. All flags must be inserted between exec and resume.
6. **IMPORTANT**: By default, append `2>/dev/null` to all `codex exec` commands to suppress thinking tokens (stderr). Only show stderr if the user explicitly requests to see thinking tokens or if debugging is needed.
7. Run the command, capture stdout/stderr (filtered as appropriate), and summarize the outcome for the user.
8. **After Codex completes**, inform the user: "You can resume this Codex session at any time by saying 'codex resume' or asking me to continue with additional analysis or changes."

### Quick Reference
| Use case | Sandbox mode | Key flags |
| --- | --- | --- |
| Read-only review or analysis | `read-only` | `--sandbox read-only 2>/dev/null` |
| Apply local edits | `workspace-write` | `--sandbox workspace-write --full-auto 2>/dev/null` |
| Permit network or broad access | `danger-full-access` | `--sandbox danger-full-access --full-auto 2>/dev/null` |
| Resume recent session | Inherited from original | `echo "prompt" \| codex exec --skip-git-repo-check resume --last 2>/dev/null` (flags go between exec and resume if needed) |
| Run from another directory | Match task needs | `-C <DIR>` plus other flags `2>/dev/null` |

## Following Up
- After every `codex` command, immediately use `AskUserQuestion` to confirm next steps, collect clarifications, or decide whether to resume with `codex exec resume --last`.
- When resuming, pipe the new prompt via stdin: `echo "new prompt" | codex exec resume --last 2>/dev/null`. The resumed session automatically uses the same model, reasoning effort, and sandbox mode from the original session.
- Restate the chosen model, reasoning effort, and sandbox mode when proposing follow-up actions.

## Error Handling
- Stop and report failures whenever `codex --version` or a `codex exec` command exits non-zero; request direction before retrying.
- Before using high-impact flags (`--full-auto`, `--sandbox danger-full-access`, `--skip-git-repo-check`), ask the user for permission using `AskUserQuestion` unless it was already given.
- When output includes warnings or partial results, summarize them and ask how to adjust using `AskUserQuestion`.

## Model Options

| Model | Best for | Context window | Key features |
| --- | --- | --- | --- |
| `gpt-5.2-max` | **Max model**: Ultra-complex reasoning, deep problem analysis | 400K input / 128K output | 76.3% SWE-bench, adaptive reasoning, $1.25/$10.00 |
| `gpt-5.2` ⭐ | **Flagship model**: Software engineering, agentic coding workflows | 400K input / 128K output | 76.3% SWE-bench, adaptive reasoning, $1.25/$10.00 |
| `gpt-5.2-mini` | Cost-efficient coding (4x more usage allowance) | 400K input / 128K output | Near SOTA performance, $0.25/$2.00 |
| `gpt-5.1-thinking` | Ultra-complex reasoning, deep problem analysis | 400K input / 128K output | Adaptive thinking depth, runs 2x slower on hardest tasks |

**GPT-5.2 Advantages**: 76.3% SWE-bench (vs 72.8% GPT-5), 30% faster on average tasks, better tool handling, reduced hallucinations, improved code quality. Knowledge cutoff: September 30, 2024.

**Reasoning Effort Levels**:
- `xhigh` - Ultra-complex tasks (deep problem analysis, complex reasoning, deep understanding of the problem)
- `high` - Complex tasks (refactoring, architecture, security analysis, performance optimization)
- `medium` - Standard tasks (refactoring, code organization, feature additions, bug fixes)
- `low` - Simple tasks (quick fixes, simple changes, code formatting, documentation)

**Cached Input Discount**: 90% off ($0.125/M tokens) for repeated context, cache lasts up to 24 hours.
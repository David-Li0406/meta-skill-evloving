---
name: codex-execution
description: Use this skill when you need to run OpenAI Codex CLI for code analysis, refactoring, or automated editing tasks.
---

# Codex Execution Skill

Orchestrate OpenAI Codex CLI for code analysis, refactoring, and automated editing tasks.

## Running a Task

1. **Ask User for Parameters**: Prompt the user to select the model (`gpt-5.2`, `gpt-5.2-codex`, etc.) and the reasoning effort (`xhigh`, `high`, `medium`, or `low`) in a single prompt.
2. **Select Sandbox Mode**: Default to `--sandbox read-only` unless edits or network access are necessary. Options include:
   - `read-only`: For analysis or review.
   - `workspace-write`: For code modifications.
   - `danger-full-access`: For system operations or network access.
3. **Assemble Command**: Build the command with the appropriate options:
   ```bash
   codex exec -m <MODEL> --config model_reasoning_effort="<LEVEL>" --sandbox <MODE> --skip-git-repo-check -C <DIR> "PROMPT"
   ```
4. **Resume Previous Session**: Use `codex exec --skip-git-repo-check resume --last` via stdin to continue a previous session. Syntax:
   ```bash
   echo "your prompt here" | codex exec --skip-git-repo-check resume --last 2>/dev/null
   ```
5. **Suppress Output**: Append `2>/dev/null` to all `codex exec` commands to suppress thinking tokens unless the user requests verbose output.
6. **Run Command**: Execute the command, capture stdout/stderr, and summarize the outcome for the user.
7. **Inform User**: After Codex completes, inform the user that they can resume the session at any time.

## Quick Reference

| Use case | Sandbox mode | Key flags |
| --- | --- | --- |
| Read-only review or analysis | `read-only` | `--sandbox read-only 2>/dev/null` |
| Apply local edits | `workspace-write` | `--sandbox workspace-write --full-auto 2>/dev/null` |
| Permit network or broad access | `danger-full-access` | `--sandbox danger-full-access --full-auto 2>/dev/null` |
| Resume recent session | Inherited from original | `echo "prompt" | codex exec --skip-git-repo-check resume --last 2>/dev/null` |
| Run from another directory | Match task needs | `-C <DIR>` plus other flags `2>/dev/null` |

## Error Handling

- **Check for Failures**: Stop and report failures whenever `codex --version` or a `codex exec` command exits non-zero; request direction before retrying.
- **User Permission for High-Impact Flags**: Before using flags like `--full-auto`, `--sandbox danger-full-access`, or `--skip-git-repo-check`, ask the user for permission unless already granted.
- **Summarize Warnings**: When output includes warnings or partial results, summarize them and ask how to adjust using `AskUserQuestion`.

## Notes

- **HPC Environment**: If running on an HPC cluster, always use the `--yolo` flag to bypass Landlock sandbox restrictions.
- **Model Options**: Default to `gpt-5.2` unless specified otherwise by the user.
- **Session Management**: Each execution returns a session ID for resuming conversations.
---
name: use-codex
description: Use when the user asks to run Codex CLI (codex exec, codex resume) or references OpenAI Codex for code analysis, refactoring, or automated editing. Triggers on "run codex", "codex analyze", "use codex for", "codex refactor", "ask codex", or when user wants OpenAI's Codex model for code tasks.
---

# Codex Skill Guide

## Running a Task

1. Use Codex's default configured model unless user explicitly requests a different one.
2. Select the sandbox mode required for the task; default to `--sandbox read-only` unless edits or network access are necessary.
3. Assemble the command with the appropriate options:
   - `-m, --model <MODEL>`
   - `--sandbox <read-only|workspace-write|danger-full-access>`
   - `--full-auto`
   - `-C <DIR>`
   - `--skip-git-repo-check`
4. Always use --skip-git-repo-check.
5. When continuing a previous session, use `codex exec --skip-git-repo-check resume --last` via stdin. Resume syntax: `codex exec --skip-git-repo-check resume --last <<< "your prompt"`. All flags must be between exec and resume.
6. Run the command, capture output, and summarize the outcome for the user.
7. **After Codex completes**, inform the user: "You can resume this Codex session at any time by saying 'codex resume'."

### Quick Reference

| Use case | Sandbox mode | Key flags |
| --- | --- | --- |
| Read-only review or analysis | `read-only` | `--sandbox read-only` |
| Apply local edits | `workspace-write` | `--sandbox workspace-write --full-auto` |
| Permit network or broad access | `danger-full-access` | `--sandbox danger-full-access --full-auto` |
| Resume recent session | Inherited | `codex exec --skip-git-repo-check resume --last <<< "prompt"` |
| Run from another directory | Match task needs | `-C <DIR>` |

## Following Up

- After every `codex` command, use `AskUserQuestion` to confirm next steps or decide whether to resume.
- When resuming, pipe the new prompt via stdin. The resumed session uses same model and sandbox from original.
- Restate the chosen model and sandbox mode when proposing follow-up actions.

## Error Handling

- Stop and report failures whenever `codex --version` or `codex exec` exits non-zero; request direction before retrying.
- Before using high-impact flags (`--full-auto`, `--sandbox danger-full-access`) ask user permission via AskUserQuestion unless already given.
- When output includes warnings or partial results, summarize and ask how to adjust.

## Helper Script

**IMPORTANT**: Always use `-f` with a temp file for prompts to avoid shell escaping issues.

```bash
# Write prompt to temp file, then run
echo 'Your prompt here (can contain "quotes", parens(), etc.)' > /tmp/codex-prompt.txt
~/.claude/skills/use-codex/scripts/codex-run.sh -f /tmp/codex-prompt.txt

# Code changes (auto-approve)
~/.claude/skills/use-codex/scripts/codex-run.sh -s workspace-write -a -f /tmp/codex-prompt.txt

# Resume session
~/.claude/skills/use-codex/scripts/codex-run.sh -r -f /tmp/codex-prompt.txt

# Capture output to file
~/.claude/skills/use-codex/scripts/codex-run.sh -a -o /tmp/result.txt -f /tmp/codex-prompt.txt
```

Run `~/.claude/skills/use-codex/scripts/codex-run.sh --help` for all options.

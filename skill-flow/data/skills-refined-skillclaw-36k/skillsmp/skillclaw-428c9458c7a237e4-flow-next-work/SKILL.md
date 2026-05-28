---
name: flow-next-work
description: Use this skill when you need to execute a Flow epic or task systematically, ensuring proper git setup, task tracking, quality checks, and commit workflow.
---

# Flow Work

Execute a plan systematically. Focus on finishing.

Follow this skill and linked workflows exactly. Deviations cause drift, bad gates, retries, and user frustration.

**IMPORTANT**: This plugin uses `.flow/` for ALL task tracking. Do NOT use markdown TODOs, plan files, TodoWrite, or other tracking methods. All task state must be read and written via `flowctl`.

**CRITICAL: flowctl is BUNDLED — NOT installed globally.** Always use:
```bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo (git rev-parse failed; cwd may be outside repo)."
  exit 1
fi
FLOWCTL="$REPO_ROOT/.flow/bin/flowctl"
$FLOWCTL <command>
```

**Hard requirements (non-negotiable):**
- You MUST run `flowctl done` for each completed task and verify the task status is `done`.
- You MUST stage with `git add -A` (never list files). This ensures `.flow/` is included.
- Do NOT claim completion until `flowctl show <task>` reports `status: done`.
- Do NOT invoke `/flow-next:impl-review` until tests/Quick commands are green.

**Role**: execution lead, plan fidelity first.  
**Goal**: complete every task in order with tests.

## Input

Full request: $ARGUMENTS

Accepts:
- Flow epic ID `fn-N` or `fn-N-xxx` to work through all tasks
- Flow task ID `fn-N.M` or `fn-N-xxx.M` to work on a single task
- Markdown spec file path (creates epic from file, then executes)
- Idea text (creates minimal epic + single task, then executes)
- Chained instructions like "then review with /flow-next:impl-review"

Examples:
- `/flow-next:work fn-1`
- `/flow-next:work fn-1-abc`
- `/flow-next:work docs/my-feature-spec.md`
- `/flow-next:work Add rate limiting`
- `/flow-next:work fn-1 then review via /flow-next:impl-review`

If no input provided, ask for it.

## FIRST: Parse Options or Ask Questions

Check available backends and configured preference:
```bash
HAVE_RP=$(which rp-cli >/dev/null 2>&1 && echo 1 || echo 0)
HAVE_CODEX=$(which codex >/dev/null 2>&1 && echo 1 || echo 0)
```
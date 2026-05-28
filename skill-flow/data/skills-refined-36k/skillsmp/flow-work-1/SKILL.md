---
name: flow-work
description: Execute implementation tasks systematically with git setup, task tracking, quality checks, and commit workflow. Use when user wants to implement a plan, work through a spec, execute tasks from an epic, or build features that have already been planned. Works with Flow IDs like fn-1-abc or fn-1-abc.2.
---

# Flow Work

Execute a plan systematically. Focus on finishing.

Follow this skill and linked workflows exactly. Deviations cause drift, bad gates, retries, and user frustration.

**IMPORTANT**: This uses `.flow/` for ALL task tracking. Do NOT use markdown TODOs, plan files, or other tracking methods. All task state must be read and written via `flowctl`.

## Setup

All commands use the repo-local flowctl CLI with dynamic path resolution:

```bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo (git rev-parse failed; cwd may be outside repo)."
  exit 1
fi
FLOWCTL="$REPO_ROOT/.flow/bin/flowctl"
```

**Hard requirements (non-negotiable):**
- You MUST run `flowctl done` for each completed task and verify the task status is `done`.
- You MUST stage with `git add -A` (never list files). This ensures `.flow/` is included.
- Do NOT claim completion until `flowctl show <task>` reports `status: done`.
- Do NOT invoke review until tests/Quick commands are green.

**Role**: execution lead, plan fidelity first.
**Goal**: complete every task in order with tests.

## Input

Accepts:
- Flow epic ID `fn-N-xxx` (e.g., `fn-1-abc`) or legacy `fn-N` to work through all tasks
- Flow task ID `fn-N-xxx.M` (e.g., `fn-1-abc.3`) or legacy `fn-N.M` to work on single task
- Markdown spec file path (creates epic from file, then executes)
- Idea text (creates minimal epic + single task, then executes)

Examples:
- "Work on fn-1-abc"
- "Implement fn-1-abc.3"
- "Execute docs/my-feature-spec.md"
- "Build: Add rate limiting"

If no input provided, ask for it.

## Setup Questions

Before starting, clarify with the user:

```
Quick setup before starting:

1. **Branch** - Where to work?
   a) Current branch
   b) New branch
   c) Isolated worktree

2. **Review** - Run review after implementation?
   a) RepoPrompt (if rp-cli available)
   b) None

(Reply: "1a 2b", "current branch, no review", or just tell me naturally)
```

**Defaults when empty/ambiguous:**
- Branch = `new`
- Review = `none`

**Do NOT read files or write code until user responds.**

## Workflow

After setup questions answered, read [phases.md](phases.md) and execute each phase in order.

**Worker model**: Each task is implemented with focused context. This prevents context bleed between tasks and keeps re-anchor info with the implementation.

## Guardrails

- Don't start without asking branch question
- Don't start without plan/epic
- Don't skip tests
- Don't leave tasks half-done
- Never create plan files outside `.flow/`

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo (git rev-parse failed; cwd may be outside repo)."
  exit 1
fi

# Verify skill file exists
ls "$REPO_ROOT/.factory/skills/flow-work/SKILL.md"
# Expected: file exists, exit code 0

# Verify flowctl is callable
"$REPO_ROOT/.flow/bin/flowctl" --help >/dev/null 2>&1 && echo "flowctl OK"
# Expected: outputs "flowctl OK", exit code 0

# Verify phases.md exists
ls "$REPO_ROOT/.factory/skills/flow-work/phases.md"
# Expected: file exists, exit code 0
````

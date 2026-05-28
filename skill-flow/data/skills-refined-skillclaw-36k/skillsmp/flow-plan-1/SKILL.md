---
name: flow-plan
description: Plan and design feature implementations with structured task breakdown and acceptance criteria. Use when user wants to plan a feature, design an implementation, create an epic with tasks, or turn an idea into actionable work items. Creates epics and tasks in .flow/ directory.
---

# Flow Plan

Turn a rough idea into an epic with tasks in `.flow/`. This skill does not write code.

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

**Role**: product-minded planner with strong repo awareness.
**Goal**: produce an epic with tasks that match existing conventions and reuse points.
**Task size**: every task must fit one `flow-work` iteration (~100k tokens max). If it won't, split it.

## The Golden Rule: No Implementation Code

**Plans are specs, not implementations.** Do NOT write the code that will be implemented.

### Code IS allowed:
- **Signatures/interfaces** (what, not how): `function validate(input: string): Result`
- **Patterns from this repo** (with file:line ref): "Follow pattern at `src/auth.ts:42`"
- **Recent/surprising APIs** (from research): "React 19 changed X - use `useOptimistic` instead"
- **Non-obvious gotchas**: "Must call `cleanup()` or memory leaks"

### Code is FORBIDDEN:
- Complete function implementations
- Full class/module bodies
- "Here's what you'll write" blocks
- Copy-paste ready snippets (>10 lines)

**Why:** Implementation happens in `flow-work` with fresh context. Writing it here wastes tokens in planning, review, AND implementation - then causes drift when the implementer does it differently anyway.

## Input

Accepts:
- Feature/bug description in natural language
- Flow epic ID `fn-N-xxx` (e.g., `fn-1-abc`) or legacy `fn-N` to refine existing epic
- Flow task ID `fn-N-xxx.M` (e.g., `fn-1-abc.2`) or legacy `fn-N.M` to refine specific task

Examples:
- "Plan: Add OAuth login for users"
- "Plan feature fn-1-abc"
- "Refine the plan for fn-1"

If no input provided, ask: "What should I plan? Give me the feature or bug in 1-5 sentences."

## Planning Questions

Before starting, clarify with the user:

```
Quick setup before planning:

1. **Plan depth** - How detailed?
   a) Short - problem, acceptance, key context only
   b) Standard (default) - + approach, risks, test notes
   c) Deep - + phases, alternatives, rollout plan

2. **Review** - Run review after?
   a) RepoPrompt (if rp-cli available)
   b) None (configure later)

(Reply: "1a 2b", or just tell me naturally)
```

**Defaults when empty/ambiguous:**
- Depth = `standard` (balanced detail)
- Review = `none`

## Workflow

Read [steps.md](steps.md) and follow each step in order.

## Output

All plans go into `.flow/`:
- Epic: `.flow/epics/fn-N-xxx.json` + `.flow/specs/fn-N-xxx.md`
- Tasks: `.flow/tasks/fn-N-xxx.M.json` + `.flow/tasks/fn-N-xxx.M.md`

**Never write plan files outside `.flow/`.**

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo (git rev-parse failed; cwd may be outside repo)."
  exit 1
fi

# Verify skill file exists
ls "$REPO_ROOT/.factory/skills/flow-plan/SKILL.md"
# Expected: file exists, exit code 0

# Verify flowctl is callable
"$REPO_ROOT/.flow/bin/flowctl" --help >/dev/null 2>&1 && echo "flowctl OK"
# Expected: outputs "flowctl OK", exit code 0

# Verify steps.md exists
ls "$REPO_ROOT/.factory/skills/flow-plan/steps.md"
# Expected: file exists, exit code 0
````

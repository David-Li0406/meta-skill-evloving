---
name: flow-impl-review
description: Review code implementations for quality, security, and architectural soundness. Use when reviewing code changes, PRs, or implementations. Conducts John Carmack-level review examining correctness, simplicity, edge cases, and security.
---

# Flow Implementation Review

Conduct a John Carmack-level review of implementation changes on the current branch.

Follow this skill and linked workflow exactly. Deviations cause drift, bad gates, retries, and user frustration.

**Role**: Code Review Coordinator (NOT the reviewer)
**Backends**: RepoPrompt (rp) via rp-cli

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

## Backend Selection

**Priority** (first match wins):
1. `--review=rp|none` argument
2. `FLOW_REVIEW_BACKEND` env var (`rp`, `none`)
3. `.flow/config.json` -> `review.backend`
4. **Error** - no auto-detection

### Parse from arguments first

Check arguments for:
- `--review=rp` or `--review rp` -> use rp
- `--review=none` or `--review none` -> skip review

If found, use that backend and skip all other detection.

### Otherwise read from config

```bash
# Priority: --review flag > env > config
BACKEND=$($FLOWCTL review-backend)

if [[ "$BACKEND" == "ASK" ]]; then
  echo "Error: No review backend configured."
  echo "Configure review.backend in .flow/config.json, or pass --review=rp|none"
  exit 1
fi

echo "Review backend: $BACKEND (override: --review=rp|none)"
```

## Critical Rules

**For rp backend:**
1. **DO NOT REVIEW CODE YOURSELF** - you coordinate, RepoPrompt reviews
2. **MUST WAIT for actual RP response** - never simulate/skip the review
3. **MUST use `flowctl rp setup-review`** - handles window selection + builder atomically
4. **DO NOT add --json flag to chat-send** - it suppresses the review response
5. **Re-reviews MUST stay in SAME chat** - omit `--new-chat` after first review

**For all backends:**
- Any failure -> inform user and stop
- Never self-declare SHIP without actual backend verdict

**FORBIDDEN**:
- Self-declaring SHIP without actual backend verdict
- Mixing backends mid-review (stick to one)
- Skipping review when backend is "none" without user consent

## Input

Arguments format: `[task ID] [--base <commit>] [focus areas]`

- `--base <commit>` - Compare against this commit instead of main/master (for task-scoped reviews)
- Task ID - Optional, for context and receipt tracking
- Focus areas - Optional, specific areas to examine

**Scope behavior:**
- With `--base`: Reviews only changes since that commit (task-scoped)
- Without `--base`: Reviews entire branch vs main/master (full branch review)

Examples:
- `fn-1-abc.2` - Review full branch for task context
- `fn-1-abc.2 --base abc123` - Review only changes since abc123
- `fn-1-abc.2 security performance` - Review with security and performance focus

## Workflow

Read [workflow.md](workflow.md) and follow each phase in order.

## Review Criteria

Conduct a John Carmack-level review examining:

1. **Correctness** - Logic errors, spec compliance
2. **Simplicity** - Over-engineering, unnecessary complexity
3. **Edge cases** - Failure modes, boundary conditions
4. **Security** - Injection, auth gaps
5. **Performance** - Hot paths, resource usage
6. **Maintainability** - Readability, documentation
7. **Tests** - Coverage, quality of test cases

Only flag issues in the changed code - not pre-existing patterns.

## Fix Loop

**CRITICAL: Do NOT ask user for confirmation. Automatically fix ALL valid issues and re-review.**

If verdict is NEEDS_WORK, loop internally until SHIP:

1. **Parse issues** from reviewer feedback (Critical -> Major -> Minor)
2. **Fix code** and run tests/lints
3. **Commit fixes** (mandatory before re-review)
4. **Re-review** (stay in same chat for RP)
5. **Repeat** until `<verdict>SHIP</verdict>`

**MAX ITERATIONS**: Limit fix+re-review cycles to 3 iterations. If still NEEDS_WORK after max rounds, inform user and stop.

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo (git rev-parse failed; cwd may be outside repo)."
  exit 1
fi

# Verify skill file exists
ls "$REPO_ROOT/.factory/skills/flow-impl-review/SKILL.md"
# Expected: file exists, exit code 0

# Verify workflow file exists
ls "$REPO_ROOT/.factory/skills/flow-impl-review/workflow.md"
# Expected: file exists, exit code 0

# Verify rp-cli availability (macOS only)
rp-cli --version 2>/dev/null || echo "rp-cli not available (non-macOS or not installed)"
# Expected: version number or degradation message

# Verify flowctl is callable
"$REPO_ROOT/.flow/bin/flowctl" --help >/dev/null 2>&1 && echo "flowctl OK"
# Expected: outputs "flowctl OK", exit code 0
````

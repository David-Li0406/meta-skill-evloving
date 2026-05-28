---
name: flow-plan-review
description: Review implementation plans with Carmack-level rigor before coding. Use when reviewing Flow epic specs, design docs, or when user wants a thorough plan review. Examines architecture, feasibility, edge cases, and task consistency.
---

# Flow Plan Review

Conduct a John Carmack-level review of epic plans before implementation.

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
1. **DO NOT REVIEW THE PLAN YOURSELF** - you coordinate, RepoPrompt reviews
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

Arguments format: `<flow-epic-id> [focus areas]`

Examples:
- `fn-1-abc` - Review epic fn-1-abc
- `fn-1-abc architecture security` - Review with focus on architecture and security

## Workflow

Read [workflow.md](workflow.md) and follow each phase in order.

## Review Criteria

Conduct a John Carmack-level review examining:

1. **Completeness** - All requirements covered? Missing edge cases?
2. **Feasibility** - Technically sound? Dependencies clear?
3. **Clarity** - Specs unambiguous? Acceptance criteria testable?
4. **Architecture** - Right abstractions? Clean boundaries?
5. **Risks** - Blockers identified? Security gaps? Mitigation?
6. **Scope** - Right-sized? Over/under-engineering?
7. **Testability** - How will we verify this works?
8. **Consistency** - Do task specs align with epic spec?

## Fix Loop

**CRITICAL: Do NOT ask user for confirmation. Automatically fix ALL valid issues and re-review.**

If verdict is NEEDS_WORK, loop internally until SHIP:

1. **Parse issues** from reviewer feedback
2. **Fix epic spec** using `$FLOWCTL epic set-plan`
3. **Sync affected task specs** using `$FLOWCTL task set-spec`
4. **Re-review** (stay in same chat for RP)
5. **Repeat** until `<verdict>SHIP</verdict>`

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo (git rev-parse failed; cwd may be outside repo)."
  exit 1
fi

# Verify skill file exists
ls "$REPO_ROOT/.factory/skills/flow-plan-review/SKILL.md"
# Expected: file exists, exit code 0

# Verify workflow file exists
ls "$REPO_ROOT/.factory/skills/flow-plan-review/workflow.md"
# Expected: file exists, exit code 0

# Verify rp-cli availability (macOS only)
rp-cli --version 2>/dev/null || echo "rp-cli not available (non-macOS or not installed)"
# Expected: version number or degradation message

# Verify flowctl is callable
"$REPO_ROOT/.flow/bin/flowctl" --help >/dev/null 2>&1 && echo "flowctl OK"
# Expected: outputs "flowctl OK", exit code 0
````

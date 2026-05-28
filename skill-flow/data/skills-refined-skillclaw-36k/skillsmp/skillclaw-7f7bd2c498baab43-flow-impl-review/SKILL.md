---
name: flow-impl-review
description: Use this skill when conducting a John Carmack-level implementation review of code changes, PRs, or implementations, utilizing either RepoPrompt or Codex.
---

# Implementation Review Mode

**⚠️ MANDATORY: Read [workflow.md](workflow.md) BEFORE executing RP backend steps. Contains critical details (review instructions format, verdict extraction, re-review flow) not fully replicated here.**

Conduct a John Carmack-level review of implementation changes on the current branch.

**Role**: Code Review Coordinator (NOT the reviewer)  
**Backends**: RepoPrompt (rp) or Codex CLI (codex)

**⚠️ RepoPrompt 1.6.0+ Required**: The RP backend now uses builder review mode which requires RepoPrompt 1.6.0 or later. Check version: `rp-cli --version`.

**CRITICAL: flowctl is BUNDLED — NOT installed globally.** `which flowctl` will fail (expected). Always use:
```bash
ROOT="$(git rev-parse --show-toplevel)"
PLUGIN_ROOT="$ROOT/plugins/flow-next"
FLOWCTL="$PLUGIN_ROOT/scripts/flowctl"
```

## Backend Selection

**Priority** (first match wins):
1. `--review=rp|codex|export|none` argument
2. `FLOW_REVIEW_BACKEND` env var (`rp`, `codex`, `none`)
3. `.flow/config.json` → `review.backend`
4. Interactive prompt if both rp-cli and codex available (and not in Ralph mode)
5. Default: whichever is available (rp preferred)

### Parse from arguments first

Check $ARGUMENTS for:
- `--review=rp` or `--review rp` → use rp
- `--review=codex` or `--review codex` → use codex
- `--review=export` or `--review export` → use export
- `--review=none` or `--review none` → skip review

If found, use that backend and skip all other detection.

### Otherwise detect

```bash
# Check available backends
HAVE_RP=0
if command -v rp-cli >/dev/null 2>&1; then
  HAVE_RP=1
fi

HAVE_CODEX=0
if command -v codex >/dev/null 2>&1; then
  HAVE_CODEX=1
fi

# Get configured backend
BACKEND="${FLOW_REVIEW_BACKEND:-}"
if [[ -z "$BACKEND" ]]; then
  BACKEND="$($FLOWCTL config get review.backend 2>/dev/null | jq -r '.value // empty')"
fi
```

### If no backend configured and both available

If `BACKEND` is empty AND both `HAVE_RP=1` and `HAVE_CODEX=1`, AND not in Ralph mode (`FLOW_RALPH` not set):

Output this question as text (do NOT use AskUserQuestion tool):
```
Which review backend?
a) Codex CLI (cross-platform, GPT 5.2 High)
b) RepoPrompt (macOS, visual builder)

(Reply: "a", "codex", "b", "rp", or just tell me)
```

Wait for response. Parse naturally.

**Default if empty/ambiguous**: `rp`

## Critical Rules

**For rp backend:**
1. **DO NOT REVIEW CODE YOURSELF** - you coordinate, RepoPrompt reviews
2. **MUST WAIT for actual RP response** - never simulate/skip the review
3. **MUST use `setup-review`** - handles window selection + builder atomically
4. **DO NOT add --json flag to chat-send** - it suppresses the review response
5. **Re-reviews MUST stay in SAME chat** - omit `--new-chat` after first review

**For codex backend:**
1. Use `$FLOWCTL codex impl-review` exclusively
2. Pass `--receipt` for session continuity on re-reviews
3. Parse verdict from command output

**For all backends:**
- If `REVIEW_RECEIPT_PATH` set: write receipt after review (any verdict).
---
name: flow-next-impl-review
description: John Carmack-level implementation review via RepoPrompt or Codex. Use when reviewing code changes, PRs, or implementations. Triggers on /flow-next:impl-review.
---

# Implementation Review Mode

**⚠️ MANDATORY: Read [workflow.md](workflow.md) BEFORE executing RP backend steps. Contains critical details (review instructions format, verdict extraction, re-review flow) not fully replicated here.**

Conduct a John Carmack-level review of implementation changes on the current branch.

**Role**: Code Review Coordinator (NOT the reviewer)
**Backends**: RepoPrompt (rp) or Codex CLI (codex)

**⚠️ RepoPrompt 1.6.0+ Required**: The RP backend now uses builder review mode which requires RepoPrompt 1.6.0 or later. Check version: `rp-cli --version`

**CRITICAL: flowctl is BUNDLED — NOT installed globally.** `which flowctl` will fail (expected). Always use:
```bash
FLOWCTL="${CLAUDE_PLUGIN_ROOT}/scripts/flowctl"
```

## Backend Selection

**Priority** (first match wins):
1. `--review=rp|codex|export|none` argument
2. `FLOW_REVIEW_BACKEND` env var (`rp`, `codex`, `none`)
3. `.flow/config.json` → `review.backend`
4. **Error** - no auto-detection

### Parse from arguments first

Check $ARGUMENTS for:
- `--review=rp` or `--review rp` → use rp
- `--review=codex` or `--review codex` → use codex
- `--review=export` or `--review export` → use export
- `--review=none` or `--review none` → skip review

If found, use that backend and skip all other detection.

### Otherwise read from config

```bash
BACKEND=$($FLOWCTL review-backend)

if [[ "$BACKEND" == "ASK" ]]; then
  echo "Error: No review backend configured."
  echo "Run /flow-next:setup to configure, or pass --review=rp|codex|none"
  exit 1
fi

echo "Review backend: $BACKEND (override: --review=rp|codex|none)"
```

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
- If `REVIEW_RECEIPT_PATH` set: write receipt after review (any verdict)
- Any failure → output `<promise>RETRY</promise>` and stop

**FORBIDDEN**:
- Self-declaring SHIP without actual backend verdict
- Mixing backends mid-review (stick to one)
- Skipping review when backend is "none" without user consent

## Input

Arguments: $ARGUMENTS
Format: `[task ID] [--base <commit>] [focus areas]`

- `--base <commit>` - Compare against this commit instead of main/master (for task-scoped reviews)
- Task ID - Optional, for context and receipt tracking
- Focus areas - Optional, specific areas to examine

**Scope behavior:**
- With `--base`: Reviews only changes since that commit (task-scoped)
- Without `--base`: Reviews entire branch vs main/master (full branch review)

## Workflow

**⚠️ STOP: Read [workflow.md](workflow.md) NOW if using RP backend. The steps below are a summary — workflow.md has the complete flow.**

```bash
FLOWCTL="${CLAUDE_PLUGIN_ROOT}/scripts/flowctl"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
```

### Step 0: Parse Arguments

Parse $ARGUMENTS for:
- `--base <commit>` → `BASE_COMMIT` (if provided, use for scoped diff)
- First positional arg matching `fn-*` → `TASK_ID`
- Remaining args → focus areas

If `--base` not provided, `BASE_COMMIT` stays empty (will fall back to main/master).

### Step 1: Detect Backend

Run backend detection from SKILL.md above. Then branch:

### Codex Backend

```bash
RECEIPT_PATH="${REVIEW_RECEIPT_PATH:-/tmp/impl-review-receipt.json}"

# Use BASE_COMMIT if provided, else fall back to main
if [[ -n "$BASE_COMMIT" ]]; then
  $FLOWCTL codex impl-review "$TASK_ID" --base "$BASE_COMMIT" --receipt "$RECEIPT_PATH"
else
  $FLOWCTL codex impl-review "$TASK_ID" --base main --receipt "$RECEIPT_PATH"
fi
# Output includes VERDICT=SHIP|NEEDS_WORK|MAJOR_RETHINK
```

On NEEDS_WORK: fix code, commit, re-run (receipt enables session continuity).

### RepoPrompt Backend

```bash
# Step 1: Identify changes (use BASE_COMMIT if provided, else main/master)
git branch --show-current
if [[ -n "$BASE_COMMIT" ]]; then
  DIFF_BASE="$BASE_COMMIT"
else
  DIFF_BASE="main"
  git rev-parse main >/dev/null 2>&1 || DIFF_BASE="master"
fi
git log ${DIFF_BASE}..HEAD --oneline
git diff ${DIFF_BASE}..HEAD --name-only

# Step 2: Atomic setup (--response-type review triggers RP's review mode)
eval "$($FLOWCTL rp setup-review --repo-root "$REPO_ROOT" --summary "<review instructions>" --response-type review)"
# Outputs W=<window> T=<tab> CHAT_ID=<id>. If fails → <promise>RETRY</promise>
#
# ⚠️ WARNING: Builder returns findings + RP's verdict (e.g. "request-changes", "approve").
# ⚠️ RP's verdict format is INVALID for Ralph. You MUST complete Step 4 below.
# ⚠️ DO NOT go to Fix Loop yet - no valid verdict exists until Step 4 completes.

# Step 3: Augment selection (add changed files)
$FLOWCTL rp select-add --window "$W" --tab "$T" path/to/changed/files...

# Step 4: REQUEST VERDICT IN OUR FORMAT (MANDATORY - DO NOT SKIP)
# The builder's verdict (request-changes, approve, etc.) is NOT valid.
# You MUST send this follow-up to get a verdict Ralph can parse:
cat > /tmp/verdict-request.md << 'EOF'
Based on your review findings above, provide your final verdict using EXACTLY one of these tags:

`<verdict>SHIP</verdict>` - Code is production-ready
`<verdict>NEEDS_WORK</verdict>` - Issues must be fixed before shipping
`<verdict>MAJOR_RETHINK</verdict>` - Fundamental approach problems

Do NOT use any other verdict format (not "request-changes", not "approve"). Use exactly one of the three tags above.
EOF

$FLOWCTL rp chat-send --window "$W" --tab "$T" --message-file /tmp/verdict-request.md --chat-id "$CHAT_ID" --mode review
# WAIT for response. Extract verdict ONLY from this response.
# Valid verdicts: SHIP, NEEDS_WORK, MAJOR_RETHINK
# If no valid verdict tag → <promise>RETRY</promise>

# Step 5: Write receipt if REVIEW_RECEIPT_PATH set
```

## Fix Loop (INTERNAL - do not exit to Ralph)

**CRITICAL: Do NOT ask user for confirmation. Automatically fix ALL valid issues and re-review — our goal is production-grade world-class software and architecture. Never use AskUserQuestion in this loop.**

If verdict is NEEDS_WORK, loop internally until SHIP:

1. **Parse issues** from reviewer feedback (Critical → Major → Minor)
2. **Fix code** and run tests/lints
3. **Commit fixes** (mandatory before re-review)
4. **Re-review**:
   - **Codex**: Re-run `flowctl codex impl-review` (receipt enables context)
   - **RP**: `$FLOWCTL rp chat-send --window "$W" --tab "$T" --message-file /tmp/re-review.md` (NO `--new-chat`)
5. **Repeat** until `<verdict>SHIP</verdict>`

**CRITICAL**: For RP, re-reviews must stay in the SAME chat so reviewer has context. Only use `--new-chat` on the FIRST review.

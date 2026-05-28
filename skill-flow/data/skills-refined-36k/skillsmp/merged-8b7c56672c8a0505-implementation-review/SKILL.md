---
name: implementation-review
description: Use this skill for conducting John Carmack-level implementation reviews via RepoPrompt or Codex, focusing on code changes, PRs, or implementations.
---

# Implementation Review Mode

**Read [workflow.md](workflow.md) for detailed phases and anti-patterns.**

Conduct a John Carmack-level review of implementation changes on the current branch.

**Role**: Code Review Coordinator (NOT the reviewer)  
**Backends**: RepoPrompt (rp), Codex CLI (codex), or OpenCode (opencode)

**CRITICAL: flowctl is BUNDLED — NOT installed globally.** Always use:
```bash
ROOT="$(git rev-parse --show-toplevel)"
PLUGIN_ROOT="$ROOT/plugins/flow-next"
FLOWCTL="$PLUGIN_ROOT/scripts/flowctl"
```

## Backend Selection

**Priority** (first match wins):
1. `--review=rp|codex|opencode|export|none` argument
2. `FLOW_REVIEW_BACKEND` env var (`rp`, `codex`, `opencode`, `none`)
3. `.flow/config.json` → `review.backend`
4. Interactive prompt if multiple backends are available (and not in Ralph mode)
5. Default: whichever is available (rp preferred)

### Parse from arguments first

Check `$ARGUMENTS` for:
- `--review=rp` or `--review rp` → use rp
- `--review=codex` or `--review codex` → use codex
- `--review=opencode` or `--review opencode` → use opencode
- `--review=export` or `--review export` → use export
- `--review=none` or `--review none` → skip review

If found, use that backend and skip all other detection.

### Otherwise detect

```bash
# Check available backends
HAVE_RP=$(which rp-cli >/dev/null 2>&1 && echo 1 || echo 0)
HAVE_CODEX=$(which codex >/dev/null 2>&1 && echo 1 || echo 0)
HAVE_OPENCODE=$(command -v opencode >/dev/null 2>&1 && echo 1 || echo 0)

# Get configured backend
BACKEND="${FLOW_REVIEW_BACKEND:-}"
if [[ -z "$BACKEND" ]]; then
  BACKEND="$($FLOWCTL config get review.backend 2>/dev/null | jq -r '.value // empty')"
fi
```

### If no backend configured and multiple available

If `BACKEND` is empty AND both `HAVE_RP=1` and `HAVE_CODEX=1`, AND not in Ralph mode (`FLOW_RALPH` not set):

Output this question as text:
```
Which review backend?
a) Codex CLI (cross-platform, GPT 5.2 High)
b) RepoPrompt (macOS, visual builder)
c) OpenCode review (GPT-5.2, reasoning high)

(Reply: "a", "codex", "b", "rp", "c", or just tell me)
```

Wait for response. Parse naturally.

**Default if empty/ambiguous**: `codex`

### If only one available or in Ralph mode

```bash
# Fallback to available
if [[ -z "$BACKEND" ]]; then
  if [[ "$HAVE_RP" == "1" ]]; then BACKEND="rp"
  elif [[ "$HAVE_CODEX" == "1" ]]; then BACKEND="codex"
  elif [[ "$HAVE_OPENCODE" == "1" ]]; then BACKEND="opencode"
  else BACKEND="none"; fi
fi
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

**For opencode backend:**
1. Use the task tool with `subagent_type: opencode-reviewer`
2. Provide full diff context (git log + changed files + diff) and focus areas
3. Parse verdict from `<verdict>...` tag
4. If `REVIEW_RECEIPT_PATH` set: write receipt JSON with `mode: "opencode"`
5. **Re-reviews must reuse the same task session**: capture `session_id` from `<task_metadata>` and pass it back via `session_id` on subsequent task tool calls

**For all backends:**
- If `REVIEW_RECEIPT_PATH` set: write receipt after review (any verdict)
- Any failure → output `<promise>RETRY</promise>` and stop

**FORBIDDEN**:
- Self-declaring SHIP without actual backend verdict
- Mixing backends mid-review (stick to one)
- Skipping review when backend is "none" without user consent

## Input

Arguments: `$ARGUMENTS`
Format: `[focus areas or task ID]`

Reviews all changes on **current branch** vs main/master.

## Workflow

**See [workflow.md](workflow.md) for full details on each backend.**

### Step 0: Detect Backend

Run backend detection from SKILL.md above. Then branch:

### Codex Backend

```bash
TASK_ID="${1:-}"
BASE_BRANCH="main"
RECEIPT_PATH="${REVIEW_RECEIPT_PATH:-/tmp/impl-review-receipt.json}"

$FLOWCTL codex impl-review "$TASK_ID" --base "$BASE_BRANCH" --receipt "$RECEIPT_PATH"
# Output includes VERDICT=SHIP|NEEDS_WORK|MAJOR_RETHINK
```

On NEEDS_WORK: fix code, commit, re-run (receipt enables session continuity).

### OpenCode Backend

```bash
TASK_ID="${1:-}"
BASE_BRANCH="main"
RECEIPT_PATH="${REVIEW_RECEIPT_PATH:-/tmp/impl-review-receipt.json}"

# Identify changes
git branch --show-current
git log main..HEAD --oneline 2>/dev/null || git log master..HEAD --oneline
git diff main..HEAD --name-only 2>/dev/null || git diff master..HEAD --name-only
DIFF_OUTPUT="$(git diff main..HEAD 2>/dev/null || git diff master..HEAD)"
```

Build a review prompt with:
- Branch + base branch
- Commit list
- Changed files
- Full diff (or a focused diff if huge)
- Focus areas from arguments
- Review criteria (correctness, security, performance, tests, risks)
- Required verdict tag

Run reviewer subagent using the task tool:
- subagent_type: `opencode-reviewer`
- prompt: `<review prompt>`

Parse verdict from reviewer response (`<verdict>SHIP|NEEDS_WORK|MAJOR_RETHINK</verdict>`).

On NEEDS_WORK: fix code, commit, re-run review (same backend).

Write receipt if `REVIEW_RECEIPT_PATH` set:
```bash
mkdir -p "$(dirname "$RECEIPT_PATH")"
ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
cat > "$RECEIPT_PATH" <<EOF
{"type":"impl_review","id":"$TASK_ID","mode":"opencode","verdict":"<VERDICT>","timestamp":"$ts"}
EOF
```

### RepoPrompt Backend

```bash
# Step 1: Identify changes
git branch --show-current
git log main..HEAD --oneline 2>/dev/null || git log master..HEAD --oneline
git diff main..HEAD --name-only 2>/dev/null || git diff master..HEAD --name-only

# Step 2: Atomic setup
eval "$($FLOWCTL rp setup-review --repo-root "$REPO_ROOT" --summary "Review implementation: <summary>")"
# Outputs W=<window> T=<tab>. If fails → <promise>RETRY</promise>

# Step 3: Augment selection
$FLOWCTL rp select-add --window "$W" --tab "$T" path/to/changed/files...

# Step 4: Build and send review prompt (see workflow.md)
$FLOWCTL rp chat-send --window "$W" --tab "$T" --message-file /tmp/review-prompt.md --new-chat --chat-name "Impl Review: [BRANCH]"

# Step 5: Write receipt if REVIEW_RECEIPT_PATH set
```

## Fix Loop (INTERNAL - do not exit to Ralph)

If verdict is NEEDS_WORK, loop internally until SHIP:

1. **Parse issues** from reviewer feedback (Critical → Major → Minor)
2. **Fix code** and run tests/lints
3. **Commit fixes** (mandatory before re-review)
4. **Re-review**:
   - **Codex**: Re-run `flowctl codex impl-review` (receipt enables context)
   - **OpenCode**: re-run reviewer subagent with updated diff
   - **RP**: `$FLOWCTL rp chat-send --window "$W" --tab "$T" --message-file /tmp/re-review.md` (NO `--new-chat`)
5. **Repeat** until `<verdict>SHIP</verdict>`

**CRITICAL**: For RP, re-reviews must stay in the SAME chat so reviewer has context. Only use `--new-chat` on the FIRST review.
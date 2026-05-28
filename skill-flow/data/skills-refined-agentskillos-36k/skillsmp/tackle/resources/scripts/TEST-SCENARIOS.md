# Tackle Scripts Test Scenarios

This document defines test cases for validating the tackle bash scripts.

## Overview

| Script | Purpose <br> @ Called From | → Inputs <br> ← Outputs |
|--------|----------------------|------------------|
| **cache-freshness.sh** | Check cache validity (24h threshold)<br>@ *Step 3 (Cache Check)* | → `ORG_REPO`<br>← `CACHE_BEAD`, `CACHE_FRESH` |
| **ci-status-check.sh** | Poll CI, detect pre-existing failures<br>@ *gate-submit* | → `PR_NUMBER`, `ORG_REPO`, `DEFAULT_BRANCH`<br>← `FAILED`, `PRE_EXISTING`, `PENDING` |
| **claim-step.sh** | Claim ownership of current molecule step<br>@ *Step 1 (Claim Step)* | → `MOL_ID`<br>← `STEP_ID` |
| **complete-step.sh** | Close step, claim next with fallback<br>@ *After each step* | → `STEP_ID`, `MOL_ID`<br>← `NEXT_STEP` |
| **complete-tackle.sh** | Close root molecule and unhook after completion<br>@ *Reflect phase (after step close)* | → `MOL_ID` (optional, recovered from hook)<br>← (closes molecule, unhooks) |
| **context-recovery.sh** | Recover IDs after session restart<br>@ *Step 10 (Context Recovery)* | → (none - reads gt hook)<br>← `ISSUE_ID`, `MOL_ID`, `ORG_REPO` |
| **detect-upstream.sh** | Detect git remote, extract org/repo<br>@ *Step 2 (Research)* | → (none - reads git config)<br>← `UPSTREAM_REMOTE`, `UPSTREAM_URL`, `ORG_REPO`, `DEFAULT_BRANCH`, `UPSTREAM_REF` |
| **env-check.sh** | Validate required env vars (BD_ACTOR, SKILL_DIR)<br>@ *Resumption Protocol* | → (reads env)<br>← (exits 1 if missing) |
| **pr-check-idempotent.sh** | Check if draft PR already exists<br>@ *gate-submit* | → `ORG_REPO`<br>← `PR_NUMBER`, `IS_DRAFT`, `PR_URL`, `BRANCH`, `FORK_OWNER` |
| **query-friction.sh** | Query molecules for friction patterns<br>@ *Reflect phase* | → (none)<br>← JSON output |
| **record-pr-stats.sh** | Calculate diff stats, update issue<br>@ *Submit phase (Record)* | → `ISSUE_ID`, `PR_URL`, `UPSTREAM_REF`<br>← `FILES_CHANGED`, `LINES_CHANGED` |
| **report-problem.sh** | Report tackle problem to mayor via mail<br>@ *When Things Go Wrong* | → `SKILL_DIR`, `STEP`, `ERROR_DESC`, `ERROR_MSG` (opt)<br>← (sends mail) |
| **sling-tackle.sh** | Sling formula, fix step parenting, claim first step<br>@ *Step 9 (Sling)* | → `ISSUE_ID`, `ORG_REPO`, `BD_ACTOR`<br>← `MOL_ID`, `FIRST_STEP` |
| **verify-pr-ready.sh** | Verify PR is no longer draft<br>@ *Submit phase* | → `PR_NUMBER`, `ORG_REPO`<br>← `IS_DRAFT`, `PR_STATE`, `PR_URL` |

---

## Quick Test Runner

Run all testable scenarios in an isolated temp repo:

```bash
#!/usr/bin/env bash
# Run from anywhere - creates isolated test environment
set -euo pipefail

SCRIPT_DIR="$HOME/.claude/skills/tackle/resources/scripts"
TEST_DIR="/tmp/tackle-test-$$"
PASSED=0
FAILED=0

cleanup() {
  rm -rf "$TEST_DIR"
  echo ""
  echo "=== Results: $PASSED passed, $FAILED failed ==="
}
trap cleanup EXIT

# Setup
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"
git init -q

test_pass() { echo "  ✅ $1"; PASSED=$((PASSED+1)); }
test_fail() { echo "  ❌ $1: $2"; FAILED=$((FAILED+1)); }

echo "=== detect-upstream.sh ==="

# Test 1: Upstream remote
git remote add upstream https://github.com/steveyegge/beads.git
source "$SCRIPT_DIR/detect-upstream.sh" 2>/dev/null
[ "$UPSTREAM_REMOTE" = "upstream" ] && [ "$ORG_REPO" = "steveyegge/beads" ] \
  && test_pass "Upstream remote" || test_fail "Upstream remote" "$ORG_REPO"

# Test 2: Fallback to origin
git remote remove upstream
git remote add origin https://github.com/testuser/testrepo.git
unset UPSTREAM_REMOTE ORG_REPO
source "$SCRIPT_DIR/detect-upstream.sh" 2>/dev/null || true
[ "$UPSTREAM_REMOTE" = "origin" ] && [ "$ORG_REPO" = "testuser/testrepo" ] \
  && test_pass "Origin fallback" || test_fail "Origin fallback" "$ORG_REPO"

# Test 3: SSH URL parsing + fork detection
git remote set-url origin git@github.com:aleiby/gastown.git
unset UPSTREAM_REMOTE ORG_REPO
source "$SCRIPT_DIR/detect-upstream.sh" 2>/dev/null || true
[ "$ORG_REPO" = "steveyegge/gastown" ] \
  && test_pass "SSH URL + fork detection" || test_fail "SSH URL + fork detection" "$ORG_REPO"

# Test 4: No remote error
git remote remove origin
git remote remove upstream 2>/dev/null || true
unset UPSTREAM_REMOTE ORG_REPO
if ! source "$SCRIPT_DIR/detect-upstream.sh" 2>&1 | grep -q "ERROR.*No git remote"; then
  test_fail "No remote error" "Expected error message"
else
  test_pass "No remote error"
fi

echo ""
echo "=== cache-freshness.sh ==="

# Test 5: No cache exists
git remote add origin https://github.com/test/test.git  # Need remote for bd commands
ORG_REPO="steveyegge/beads"
unset CACHE_BEAD CACHE_FRESH
source "$SCRIPT_DIR/cache-freshness.sh" 2>/dev/null || true
[ -z "$CACHE_BEAD" ] && [ "$CACHE_FRESH" = "false" ] \
  && test_pass "No cache exists" || test_fail "No cache exists" "CACHE_FRESH=$CACHE_FRESH"

echo ""
echo "=== claim-step.sh ==="

# Test 6: No hook (graceful empty)
MOL_ID="test-mol-123"
unset STEP_ID
source "$SCRIPT_DIR/claim-step.sh" 2>/dev/null || true
[ -z "$STEP_ID" ] \
  && test_pass "No hook (empty STEP_ID)" || test_fail "No hook" "STEP_ID=$STEP_ID"

echo ""
echo "=== context-recovery.sh ==="

# Test 7: No hook/remote error (remove all remotes so fallback also fails)
git remote remove origin 2>/dev/null || true
git remote remove upstream 2>/dev/null || true
RECOVERY_OUT=$(bash "$SCRIPT_DIR/context-recovery.sh" 2>&1 || true)
if echo "$RECOVERY_OUT" | grep -q "ERROR.*No upstream"; then
  test_pass "No hook/remote error"
else
  test_fail "No hook/remote error" "Got: $RECOVERY_OUT"
fi
# Restore remote for subsequent tests
git remote add origin https://github.com/test/test.git

echo ""
echo "=== pr-check-idempotent.sh ==="

# Test 8: No existing PR
git checkout -b test-branch 2>/dev/null || true
ORG_REPO="steveyegge/gastown"
git remote set-url origin https://github.com/aleiby/gastown.git
unset PR_NUMBER BRANCH FORK_OWNER
source "$SCRIPT_DIR/pr-check-idempotent.sh" 2>/dev/null || true
[ -z "$PR_NUMBER" ] && [ "$BRANCH" = "test-branch" ] && [ "$FORK_OWNER" = "aleiby" ] \
  && test_pass "No existing PR" || test_fail "No existing PR" "FORK_OWNER=$FORK_OWNER"

echo ""
echo "=== complete-step.sh ==="

# Test 9: Invalid context (expected failure) - must export vars for bash subshell
export STEP_ID="test-step" MOL_ID="test-mol"
COMPLETE_OUT=$(bash "$SCRIPT_DIR/complete-step.sh" 2>&1 || true)
if echo "$COMPLETE_OUT" | grep -qE "(resolving ID|operation failed|no issue found|no beads database)"; then
  test_pass "Invalid context error"
else
  test_fail "Invalid context error" "Got: $COMPLETE_OUT"
fi
unset STEP_ID MOL_ID

echo ""
echo "=== ci-status-check.sh (using steveyegge/gastown) ==="

# Test 10: Real PR with CI checks
PR_NUMBER=893  # A closed PR with completed CI
ORG_REPO="steveyegge/gastown"
DEFAULT_BRANCH="main"
unset FAILED PRE_EXISTING PENDING
source "$SCRIPT_DIR/ci-status-check.sh" 2>/dev/null || true
[ "$FAILED" -gt 0 ] && [ "$PRE_EXISTING" = "true" ] \
  && test_pass "CI status check (pre-existing failures)" || test_fail "CI status check" "FAILED=$FAILED PRE_EXISTING=$PRE_EXISTING"

echo ""
echo "=== cache-freshness.sh (with real cache bead) ==="

# Test 11-12: Cache tests require beads workspace - run from ~/gt
pushd ~/gt >/dev/null 2>&1 || { echo "  ⏭️ Cache tests skipped (no ~/gt)"; }
if [ "$(pwd)" = "$HOME/gt" ]; then
  CACHE_ID=$(bd create --title="Cache: test/repo" --label=tackle-cache --notes="last_checked: $(date -Iseconds)" --json 2>/dev/null | jq -r '.id // empty')
  if [ -n "$CACHE_ID" ]; then
    ORG_REPO="test/repo"
    unset CACHE_BEAD CACHE_FRESH
    source "$SCRIPT_DIR/cache-freshness.sh" 2>/dev/null || true
    [ "$CACHE_FRESH" = "true" ] \
      && test_pass "Fresh cache detected" || test_fail "Fresh cache" "CACHE_FRESH=$CACHE_FRESH"

    # Test 12: Stale cache (update to old timestamp)
    bd update "$CACHE_ID" --notes="last_checked: 2026-01-01T00:00:00Z" >/dev/null 2>&1
    unset CACHE_BEAD CACHE_FRESH
    source "$SCRIPT_DIR/cache-freshness.sh" 2>/dev/null || true
    [ "$CACHE_FRESH" = "false" ] \
      && test_pass "Stale cache detected" || test_fail "Stale cache" "CACHE_FRESH=$CACHE_FRESH"

    # Cleanup
    bd close "$CACHE_ID" --reason "Test cleanup" >/dev/null 2>&1
  else
    test_fail "Cache bead creation" "Could not create bead"
  fi
  popd >/dev/null 2>&1
fi

echo ""
echo "=== verify-pr-ready.sh ==="

# Test 13: Verify closed PR (not draft)
PR_NUMBER=893
ORG_REPO="steveyegge/gastown"
unset IS_DRAFT PR_STATE PR_URL
source "$SCRIPT_DIR/verify-pr-ready.sh" 2>/dev/null || true
[ "$IS_DRAFT" = "false" ] && [ "$PR_STATE" = "CLOSED" ] \
  && test_pass "Verify PR ready (closed PR)" || test_fail "Verify PR ready" "IS_DRAFT=$IS_DRAFT PR_STATE=$PR_STATE"

echo ""
echo "=== query-friction.sh ==="

# Test 14: Query friction requires beads workspace - run from ~/gt
pushd ~/gt >/dev/null 2>&1 || { echo "  ⏭️ Query friction skipped (no ~/gt)"; }
if [ "$(pwd)" = "$HOME/gt" ]; then
  if bash "$SCRIPT_DIR/query-friction.sh" >/dev/null 2>&1; then
    test_pass "Query friction (runs without error)"
  else
    test_fail "Query friction" "Script failed"
  fi
  popd >/dev/null 2>&1
fi

echo ""
echo "=== record-pr-stats.sh ==="

# Test 15: Missing required variables (should error)
unset ISSUE_ID PR_URL UPSTREAM_REF
RECORD_OUT=$(bash "$SCRIPT_DIR/record-pr-stats.sh" 2>&1 || true)
if echo "$RECORD_OUT" | grep -q "ERROR.*ISSUE_ID"; then
  test_pass "Missing ISSUE_ID error"
else
  test_fail "Missing ISSUE_ID error" "Got: $RECORD_OUT"
fi

echo ""
echo "=== report-problem.sh ==="

# Test 16: Missing STEP variable (should error)
unset STEP ERROR_DESC ERROR_MSG
export SKILL_DIR="$SCRIPT_DIR/.."
REPORT_OUT=$(bash "$SCRIPT_DIR/report-problem.sh" 2>&1 || true)
if echo "$REPORT_OUT" | grep -q "ERROR.*STEP"; then
  test_pass "Missing STEP error"
else
  test_fail "Missing STEP error" "Got: $REPORT_OUT"
fi

echo ""
echo "=== env-check.sh ==="

# Test 17: Missing BD_ACTOR (should error)
unset BD_ACTOR
export SKILL_DIR="$SCRIPT_DIR/.."
ENV_OUT=$(bash "$SCRIPT_DIR/env-check.sh" 2>&1 || true)
if echo "$ENV_OUT" | grep -q "Missing required" && echo "$ENV_OUT" | grep -q "BD_ACTOR"; then
  test_pass "Missing BD_ACTOR error"
else
  test_fail "Missing BD_ACTOR error" "Got: $ENV_OUT"
fi

# Test 18: Missing SKILL_DIR (should error)
unset SKILL_DIR
export BD_ACTOR="test/actor"
ENV_OUT=$(bash "$SCRIPT_DIR/env-check.sh" 2>&1 || true)
if echo "$ENV_OUT" | grep -q "Missing required" && echo "$ENV_OUT" | grep -q "SKILL_DIR"; then
  test_pass "Missing SKILL_DIR error"
else
  test_fail "Missing SKILL_DIR error" "Got: $ENV_OUT"
fi

# Test 19: All vars set (should pass)
export BD_ACTOR="test/actor"
export SKILL_DIR="$SCRIPT_DIR/.."
ENV_OUT=$(bash "$SCRIPT_DIR/env-check.sh" 2>&1)
if echo "$ENV_OUT" | grep -q "Environment OK"; then
  test_pass "All env vars present"
else
  test_fail "All env vars present" "Got: $ENV_OUT"
fi

echo ""
echo "=== complete-tackle.sh ==="

# Test 20: No MOL_ID and no hook (should error)
unset MOL_ID
# Create a wrapper script that mocks gt and sources complete-tackle.sh
COMPLETE_OUT=$(bash -c "
  gt() { echo '{}'; }
  export -f gt
  MOL_ID=''
  source '$SCRIPT_DIR/complete-tackle.sh'
" 2>&1 || true)
if echo "$COMPLETE_OUT" | grep -q "ERROR.*No molecule ID"; then
  test_pass "No MOL_ID error"
else
  test_fail "No MOL_ID error" "Got: $COMPLETE_OUT"
fi

echo ""
echo "=== TESTS REQUIRING ACTIVE MOLECULE (not run) ==="
echo "  - claim-step.sh / complete-step.sh with active molecule"
echo "  - complete-tackle.sh with active molecule (close + unhook)"
echo "  - report-problem.sh full send (needs mail infrastructure)"
```

---

## Manual Test Cases

### detect-upstream.sh

#### Test 1: Upstream remote exists
```bash
cd /tmp/tackle-test && git init
git remote add upstream https://github.com/steveyegge/beads.git
source ~/.claude/skills/tackle/resources/scripts/detect-upstream.sh
echo "UPSTREAM_REMOTE=$UPSTREAM_REMOTE ORG_REPO=$ORG_REPO"
# Expected: UPSTREAM_REMOTE=upstream ORG_REPO=steveyegge/beads
```

#### Test 2: Fallback to origin
```bash
git remote remove upstream
git remote add origin https://github.com/testuser/testrepo.git
source ~/.claude/skills/tackle/resources/scripts/detect-upstream.sh
echo "UPSTREAM_REMOTE=$UPSTREAM_REMOTE ORG_REPO=$ORG_REPO"
# Expected: UPSTREAM_REMOTE=origin ORG_REPO=testuser/testrepo
```

#### Test 3: SSH URL + fork detection
```bash
git remote set-url origin git@github.com:aleiby/gastown.git
source ~/.claude/skills/tackle/resources/scripts/detect-upstream.sh
echo "ORG_REPO=$ORG_REPO"
# Expected: Detects fork, ORG_REPO=steveyegge/gastown
```

#### Test 4: No remote (error case)
```bash
git remote remove origin
git remote remove upstream 2>/dev/null
source ~/.claude/skills/tackle/resources/scripts/detect-upstream.sh
# Expected: Exit 1 with "ERROR: No git remote found"
```

---

### cache-freshness.sh

#### Test 1: No cache exists
```bash
ORG_REPO="steveyegge/beads"
source ~/.claude/skills/tackle/resources/scripts/cache-freshness.sh
echo "CACHE_BEAD=$CACHE_BEAD CACHE_FRESH=$CACHE_FRESH"
# Expected: CACHE_BEAD= CACHE_FRESH=false
```

#### Test 2: Fresh cache (requires beads setup)
```bash
# Create cache bead with recent timestamp
bd create --title="Cache: org/repo" --label=tackle-cache --notes="last_checked: $(date -Iseconds)"
ORG_REPO="org/repo"
source ~/.claude/skills/tackle/resources/scripts/cache-freshness.sh
# Expected: CACHE_FRESH=true
```

---

### claim-step.sh

#### Test 1: No active hook
```bash
MOL_ID="test-mol-123"
source ~/.claude/skills/tackle/resources/scripts/claim-step.sh
echo "STEP_ID=$STEP_ID"
# Expected: STEP_ID= (empty, no error)
```

#### Test 2: With active molecule (requires Gas Town)
```bash
# Must have work on hook with attached molecule
MOL_ID=$(gt hook --json | jq -r '.attached_molecule')
source ~/.claude/skills/tackle/resources/scripts/claim-step.sh
echo "STEP_ID=$STEP_ID"
# Expected: STEP_ID=gt-wisp-xxx (first ready step)
```

---

### context-recovery.sh

#### Test 1: No hook (error case)
```bash
source ~/.claude/skills/tackle/resources/scripts/context-recovery.sh
# Expected: Exit 1 with "ERROR: No upstream found in issue notes"
```

#### Test 2: With active tackle (requires Gas Town)
```bash
# Must have tackle in progress
source ~/.claude/skills/tackle/resources/scripts/context-recovery.sh
echo "ISSUE_ID=$ISSUE_ID MOL_ID=$MOL_ID ORG_REPO=$ORG_REPO"
# Expected: All three variables set from hook data
```

---

### pr-check-idempotent.sh

#### Test 1: No existing PR
```bash
git checkout -b test-branch
ORG_REPO="steveyegge/gastown"
source ~/.claude/skills/tackle/resources/scripts/pr-check-idempotent.sh
echo "PR_NUMBER=$PR_NUMBER BRANCH=$BRANCH FORK_OWNER=$FORK_OWNER"
# Expected: PR_NUMBER= BRANCH=test-branch FORK_OWNER=<your-username>
```

#### Test 2: Existing draft PR (requires real PR)
```bash
# Create draft PR first, then run
ORG_REPO="steveyegge/gastown"
source ~/.claude/skills/tackle/resources/scripts/pr-check-idempotent.sh
echo "PR_NUMBER=$PR_NUMBER IS_DRAFT=$IS_DRAFT"
# Expected: PR_NUMBER=<number> IS_DRAFT=true
```

---

### ci-status-check.sh

Uses steveyegge/gastown for live testing.

#### Test 1: PR with pre-existing failures
```bash
PR_NUMBER=893  # Closed PR with completed CI
ORG_REPO="steveyegge/gastown"
DEFAULT_BRANCH="main"
source ~/.claude/skills/tackle/resources/scripts/ci-status-check.sh
echo "FAILED=$FAILED PRE_EXISTING=$PRE_EXISTING PENDING=$PENDING"
# Expected: FAILED=2 PRE_EXISTING=true PENDING=0
```

#### Test 2: Find a PR with passing CI
```bash
# List recent PRs to find one with passing checks
gh pr list --repo steveyegge/gastown --state merged --limit 5 --json number,title
PR_NUMBER=<pick-one>
ORG_REPO="steveyegge/gastown"
DEFAULT_BRANCH="main"
source ~/.claude/skills/tackle/resources/scripts/ci-status-check.sh
echo "FAILED=$FAILED PRE_EXISTING=$PRE_EXISTING"
# Expected: FAILED=0 PRE_EXISTING=false
```

---

### complete-step.sh

#### Test 1: No beads DB (error case)
```bash
STEP_ID="test-step" MOL_ID="test-mol"
bash ~/.claude/skills/tackle/resources/scripts/complete-step.sh
# Expected: Exit 1 with "no beads database found"
```

#### Test 2: With active molecule (requires Gas Town)
```bash
STEP_ID=$(bd --no-daemon mol current --json | jq -r '.current_step.id')
MOL_ID=$(gt hook --json | jq -r '.attached_molecule')
source ~/.claude/skills/tackle/resources/scripts/complete-step.sh
echo "NEXT_STEP=$NEXT_STEP"
# Expected: Current step closed, NEXT_STEP set to next ready step
```

---

### complete-tackle.sh

#### Test 1: No MOL_ID and no hook (error case)
```bash
unset MOL_ID
# Mock gt to return empty hook
gt() { echo "{}"; }
export -f gt
source ~/.claude/skills/tackle/resources/scripts/complete-tackle.sh
# Expected: Exit 1 with "ERROR: No molecule ID found"
```

#### Test 2: With active molecule (requires Gas Town)
```bash
# Should have an active tackle molecule on hook
gt hook  # Verify molecule attached
source ~/.claude/skills/tackle/resources/scripts/complete-tackle.sh
# Expected: Molecule closed, "No molecules in progress" shown, hook cleared
gt hook  # Should show nothing hooked
```

---

### verify-pr-ready.sh

#### Test 1: Closed PR (not draft)
```bash
PR_NUMBER=893
ORG_REPO="steveyegge/gastown"
source ~/.claude/skills/tackle/resources/scripts/verify-pr-ready.sh
echo "IS_DRAFT=$IS_DRAFT PR_STATE=$PR_STATE"
# Expected: IS_DRAFT=false PR_STATE=CLOSED
```

#### Test 2: Draft PR (should error)
```bash
# Find a draft PR first
gh pr list --repo steveyegge/gastown --state open --json number,isDraft | jq '.[] | select(.isDraft)'
PR_NUMBER=<draft-pr-number>
ORG_REPO="steveyegge/gastown"
source ~/.claude/skills/tackle/resources/scripts/verify-pr-ready.sh
# Expected: Exit 1 with "ERROR: PR #xxx still in draft"
```

---

### record-pr-stats.sh

#### Test 1: Record stats for real issue
```bash
# Requires active tackle with git changes
ISSUE_ID="<your-issue-id>"
PR_URL="https://github.com/org/repo/pull/123"
UPSTREAM_REF="upstream/main"
source ~/.claude/skills/tackle/resources/scripts/record-pr-stats.sh
echo "FILES_CHANGED=$FILES_CHANGED LINES_CHANGED=$LINES_CHANGED"
# Expected: Updates issue, prints stats
```

---

### query-friction.sh

#### Test 1: Query friction patterns
```bash
bash ~/.claude/skills/tackle/resources/scripts/query-friction.sh
# Expected: JSON output of closed tackle molecules with friction
# May be empty if no friction recorded
```

---

## Cleanup

After testing, remove the temp repo:

```bash
rm -rf /tmp/tackle-test
# Or if using PID-based name:
rm -rf /tmp/tackle-test-*
```

---

## Cross-Platform Testing

For `cache-freshness.sh`, the date parsing handles both:
- **Linux (GNU date)**: `date -d "$TIMESTAMP" +%s`
- **macOS (BSD date)**: `date -j -f "%Y-%m-%dT%H:%M:%S" "$BARE_TS" +%s`

Test timestamps to verify:
- `2024-01-15T10:30:00+00:00` (with timezone offset)
- `2024-01-15T10:30:00Z` (with Z suffix)
- `2024-01-15T10:30:00` (bare timestamp)

---

## sling-tackle.sh

### Known Issues: Molecule Step Linking

**Bugs (cannot be worked around in tackle):**
- bd-69d7: gt sling --on adds root molecule as BLOCKING dep instead of parent-child
- bd-v29h: `bd update --parent` silently fails on wisps (parent_id stays null)

**Impact:** Steps are linked to molecules via blocking deps instead of parent-child. This means:
- `bd list --parent` and `bd ready --parent` don't work
- Must use `gt hook --json` or `bd dep list --type=blocks` to find steps

**Key command to find steps:**
```bash
# Find steps via blocking deps (the only link that exists)
bd dep list "$MOL_ID" --direction=up --type=blocks --json | jq -r '.[].id // empty'
```

**Test: Verify steps are findable via blocking deps:**
```bash
# After gt sling tackle --on <issue>
HOOK_JSON=$(gt hook --json)
MOL_ID=$(echo "$HOOK_JSON" | jq -r '.attached_molecule')

# Primary: gt hook has step data
echo "$HOOK_JSON" | jq '.progress.ready_steps'  # Should list step IDs

# Fallback: blocking deps link steps to molecule
bd dep list "$MOL_ID" --direction=up --type=blocks --json | jq -r '.[].id'  # Should list step IDs
```

---

## Test Results Log

Last tested: 2026-01-23

| Script | Test | Result |
|--------|------|--------|
| detect-upstream.sh | Upstream remote | ✅ |
| detect-upstream.sh | Origin fallback | ✅ |
| detect-upstream.sh | SSH URL + fork detection | ✅ |
| detect-upstream.sh | No remote error | ✅ |
| cache-freshness.sh | No cache exists | ✅ |
| cache-freshness.sh | Fresh cache (real bead) | ✅ |
| cache-freshness.sh | Stale cache (real bead) | ✅ |
| claim-step.sh | No hook (graceful) | ✅ |
| context-recovery.sh | No hook/remote error | ✅ |
| pr-check-idempotent.sh | No existing PR | ✅ |
| complete-step.sh | Invalid context error | ✅ |
| ci-status-check.sh | Real PR #893 (pre-existing failures) | ✅ |
| verify-pr-ready.sh | Closed PR (not draft) | ✅ |
| query-friction.sh | Runs without error | ✅ |
| record-pr-stats.sh | Missing ISSUE_ID error | ✅ |
| report-problem.sh | Missing STEP error | ✅ |

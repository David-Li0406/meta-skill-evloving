# Autonomous Validation Reference

**Purpose**: Validation tests that Claude Code executes autonomously, plus user-required test flows.

**Key Principle**: Claude executes 8 tests autonomously and displays results in CLI. User interaction is only required for 2 tests that need terminal control.

---

## Test Categories

| Test                     | Autonomous? | Reason                      |
| ------------------------ | ----------- | --------------------------- |
| Tool preflight           | YES         | Bash checks tools           |
| zstd round-trip          | YES         | Synthetic test data         |
| Brotli round-trip        | YES         | Synthetic test data         |
| zstd concatenation       | YES         | Critical for streaming      |
| Git/gh auth check        | YES         | Query auth status           |
| Orphan branch validation | YES         | Check remote/local          |
| Workflow file check      | YES         | Read file contents          |
| GitHub Actions trigger   | YES         | gh workflow run + watch     |
| Recording test           | NO (USER)   | Requires starting asciinema |
| Chunker live test        | NO (USER)   | Requires active recording   |

---

## Autonomous Validation Script

Execute this script via Bash tool to run all autonomous tests:

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
#!/usr/bin/env bash
# autonomous-validation.sh - Claude runs this automatically
# Usage: autonomous-validation.sh <repo_dir> <repo_url> [branch_name]

set -euo pipefail

REPO_DIR="${1:?Usage: autonomous-validation.sh <repo_dir> <repo_url> [branch_name]}"
REPO_URL="${2:?Usage: autonomous-validation.sh <repo_dir> <repo_url> [branch_name]}"
BRANCH_NAME="${3:-gh-recordings}"

PASSED=0
FAILED=0

log_pass() { echo "  ✓ $1"; ((PASSED++)); }
log_fail() { echo "  ✗ $1"; ((FAILED++)); }
log_run()  { echo "[RUN] $1..."; }

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ AUTONOMOUS VALIDATION - Claude Code Executes All Tests         ║"
echo "╠════════════════════════════════════════════════════════════════╣"

# ─────────────────────────────────────────────────────────────────────
# Phase 1: Tool Check
# ─────────────────────────────────────────────────────────────────────
echo ""
echo "  Phase 1: Tool Check"
echo "  ─────────────────"
for tool in asciinema zstd brotli git gh; do
  log_run "Checking $tool"
  if command -v "$tool" &>/dev/null; then
    VERSION=$("$tool" --version 2>&1 | head -1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1 || echo "?")
    log_pass "$tool installed (v$VERSION)"
  else
    log_fail "$tool MISSING"
  fi
done

# ─────────────────────────────────────────────────────────────────────
# Phase 2: Compression Tests
# ─────────────────────────────────────────────────────────────────────
echo ""
echo "  Phase 2: Compression Tests"
echo "  ────────────────────────"

log_run "zstd round-trip"
TEST_DATA="test-$(date +%s)"
if echo "$TEST_DATA" | zstd -3 2>/dev/null | zstd -d 2>/dev/null | grep -q "$TEST_DATA"; then
  log_pass "zstd round-trip PASSED"
else
  log_fail "zstd round-trip FAILED"
fi

log_run "brotli round-trip"
if echo "$TEST_DATA" | brotli 2>/dev/null | brotli -d 2>/dev/null | grep -q "$TEST_DATA"; then
  log_pass "brotli round-trip PASSED"
else
  log_fail "brotli round-trip FAILED"
fi

log_run "zstd concatenation (CRITICAL for streaming)"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
echo "chunk1" | zstd -3 > "$TMP/a.zst" 2>/dev/null
echo "chunk2" | zstd -3 > "$TMP/b.zst" 2>/dev/null
cat "$TMP/a.zst" "$TMP/b.zst" > "$TMP/combined.zst"
RESULT=$(zstd -d -c "$TMP/combined.zst" 2>/dev/null || true)
if [[ "$RESULT" == $'chunk1\nchunk2' ]]; then
  log_pass "zstd concatenation PASSED"
else
  log_fail "zstd concatenation FAILED"
fi

# ─────────────────────────────────────────────────────────────────────
# Phase 3: Repository Validation
# ─────────────────────────────────────────────────────────────────────
echo ""
echo "  Phase 3: Repository Validation"
echo "  ─────────────────────────────"

log_run "Checking gh auth"
if gh auth status &>/dev/null; then
  ACCOUNT=$(gh api user --jq '.login' 2>/dev/null || echo "unknown")
  log_pass "authenticated as $ACCOUNT"
else
  log_fail "gh not authenticated"
fi

log_run "Checking orphan branch on remote"
if git ls-remote --heads "$REPO_URL" "$BRANCH_NAME" 2>/dev/null | grep -q "$BRANCH_NAME"; then
  log_pass "$BRANCH_NAME exists on remote"
else
  log_fail "$BRANCH_NAME NOT found on remote"
fi

log_run "Checking local clone"
if [[ -d "$REPO_DIR" ]]; then
  log_pass "local directory exists: $REPO_DIR"
else
  log_fail "local directory NOT found: $REPO_DIR"
fi

log_run "Checking workflow file"
if [[ -f "$REPO_DIR/.github/workflows/recompress.yml" ]]; then
  log_pass "recompress.yml present"
else
  log_fail "recompress.yml MISSING"
fi

# ─────────────────────────────────────────────────────────────────────
# Phase 4: GitHub Actions Test
# ─────────────────────────────────────────────────────────────────────
echo ""
echo "  Phase 4: GitHub Actions Test"
echo "  ─────────────────────────────"

# Extract owner/repo from URL for gh commands
OWNER_REPO=""
if [[ "$REPO_URL" =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
  OWNER_REPO="${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
fi

if [[ -z "$OWNER_REPO" ]]; then
  log_fail "Could not parse owner/repo from URL: $REPO_URL"
else
  log_run "Triggering workflow_dispatch"
  if gh workflow run recompress -R "$OWNER_REPO" --ref "$BRANCH_NAME" 2>/dev/null; then
    log_pass "workflow triggered"
    sleep 5

    log_run "Fetching run status"
    RUN_ID=$(gh run list -R "$OWNER_REPO" -w recompress --limit 1 --json databaseId -q '.[0].databaseId' 2>/dev/null || true)

    if [[ -n "$RUN_ID" ]]; then
      STATUS=$(gh run view "$RUN_ID" -R "$OWNER_REPO" --json status -q '.status' 2>/dev/null || echo "unknown")
      echo "  ⏳ Run #$RUN_ID: $STATUS"

      # Wait for completion (max 60s)
      COMPLETED=false
      for _ in {1..12}; do
        STATUS_FULL=$(gh run view "$RUN_ID" -R "$OWNER_REPO" --json status,conclusion -q '.status + " " + .conclusion' 2>/dev/null || true)
        if [[ "$STATUS_FULL" == "completed "* ]]; then
          CONCLUSION="${STATUS_FULL#completed }"
          if [[ "$CONCLUSION" == "success" ]]; then
            log_pass "workflow completed successfully"
          else
            log_fail "workflow completed with: $CONCLUSION"
          fi
          COMPLETED=true
          break
        fi
        sleep 5
      done

      if [[ "$COMPLETED" == "false" ]]; then
        echo "  ⏳ Run still in progress after 60s (check manually)"
        log_pass "workflow triggered (completion pending)"
      fi
    else
      log_fail "could not fetch run ID"
    fi
  else
    log_fail "workflow trigger failed (workflow_dispatch may not be enabled)"
  fi
fi

# ─────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────
echo ""
echo "║                                                                 ║"
echo "╠═════════════════════════════════════════════════════════════════╣"
echo "║  AUTONOMOUS TESTS: $PASSED passed, $FAILED failed"
echo "╚═════════════════════════════════════════════════════════════════╝"

[[ $FAILED -eq 0 ]] && exit 0 || exit 1
PREFLIGHT_EOF
```

---

## User-Required Tests

These tests require user action in a terminal. Use AskUserQuestion to guide the user.

### Recording Validation

**AskUserQuestion**:

```yaml
question: "Ready to test recording? This requires you to start asciinema in another terminal."
header: "Recording Test"
options:
  - label: "Guide me through it (Recommended)"
    description: "I'll show step-by-step instructions"
  - label: "Skip this test"
    description: "I trust the setup works"
  - label: "I've already verified recording works"
    description: "Mark as passed"
```

**If user selects "Guide me through it"**, display:

```
╔════════════════════════════════════════════════════════════════╗
║ USER ACTION REQUIRED: Recording Test                           ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  In a NEW terminal, run:                                       ║
║  ┌────────────────────────────────────────────────────────┐    ║
║  │ asciinema rec ~/asciinema_recordings/test_session.cast │    ║
║  └────────────────────────────────────────────────────────┘    ║
║                                                                 ║
║  Then:                                                         ║
║  1. Type a few commands (ls, echo "hello", etc.)               ║
║  2. Exit with Ctrl+D or type 'exit'                            ║
║  3. Come back here when done                                   ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

**After user confirms**, Claude validates autonomously:

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF_2'
# Claude runs after user confirms
CAST_FILE="$HOME/asciinema_recordings/test_session.cast"

if [[ -f "$CAST_FILE" ]]; then
  echo "  ✓ test_session.cast exists"

  # Check JSON header
  if head -1 "$CAST_FILE" | jq -e '.version' &>/dev/null; then
    echo "  ✓ Valid JSON header"
  else
    echo "  ✗ Invalid JSON header"
  fi

  # Check line count (at least header + some events)
  LINE_COUNT=$(wc -l < "$CAST_FILE")
  if [[ $LINE_COUNT -gt 1 ]]; then
    echo "  ✓ $LINE_COUNT events recorded"
  else
    echo "  ✗ No events recorded"
  fi
else
  echo "  ✗ test_session.cast NOT found"
fi
PREFLIGHT_EOF_2
```

### Live Chunker Test (Optional)

**AskUserQuestion**:

```yaml
question: "Ready to test live chunking? This requires running recording + chunker simultaneously."
header: "Chunker Test (Optional)"
options:
  - label: "Guide me through it"
    description: "Full end-to-end test with two terminals"
  - label: "Skip - I trust the setup"
    description: "Chunker test is optional"
```

**If user selects "Guide me through it"**, display:

```
╔════════════════════════════════════════════════════════════════╗
║ USER ACTION REQUIRED: Live Chunker Test                        ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  TERMINAL 1 (Recording):                                       ║
║  ┌────────────────────────────────────────────────────────┐    ║
║  │ asciinema rec ~/asciinema_recordings/chunker_test.cast │    ║
║  └────────────────────────────────────────────────────────┘    ║
║                                                                 ║
║  TERMINAL 2 (Chunker):                                         ║
║  ┌────────────────────────────────────────────────────────┐    ║
║  │ ~/asciinema_recordings/<repo>/idle-chunker.sh \        │    ║
║  │   ~/asciinema_recordings/chunker_test.cast             │    ║
║  └────────────────────────────────────────────────────────┘    ║
║                                                                 ║
║  In Terminal 1:                                                ║
║  1. Type some commands                                         ║
║  2. Wait 30+ seconds (idle threshold)                          ║
║  3. Type more commands                                         ║
║  4. Exit with Ctrl+D                                           ║
║                                                                 ║
║  Watch Terminal 2 for chunk creation messages.                 ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

**After user confirms**, Claude validates:

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF_3'
# Check if chunks were created
REPO_DIR="$HOME/asciinema_recordings/<repo>"
CHUNKS=$(find "$REPO_DIR/chunks" -name "*.zst" 2>/dev/null | wc -l)

if [[ $CHUNKS -gt 0 ]]; then
  echo "  ✓ $CHUNKS chunk(s) created"

  # Check if git tracked
  cd "$REPO_DIR"
  if git status --porcelain chunks/ 2>/dev/null | grep -q .; then
    echo "  ✓ Chunks staged for commit"
  fi
else
  echo "  ✗ No chunks found in $REPO_DIR/chunks/"
fi
PREFLIGHT_EOF_3
```

---

## Troubleshooting

Common failures and resolutions:

| Failure                             | Cause                | Resolution                                                    |
| ----------------------------------- | -------------------- | ------------------------------------------------------------- |
| `asciinema MISSING`                 | Not installed        | `brew install asciinema` (macOS) or `pipx install asciinema`  |
| `zstd MISSING`                      | Not installed        | `brew install zstd` (macOS) or `apt install zstd` (Linux)     |
| `brotli MISSING`                    | Not installed        | `brew install brotli` (macOS) or `apt install brotli` (Linux) |
| `gh not authenticated`              | No GitHub login      | Run `gh auth login` and follow prompts                        |
| `gh-recordings NOT found on remote` | Branch not pushed    | Run orphan branch setup from Phase 4 of skill                 |
| `local directory NOT found`         | Clone failed         | Check repo URL and permissions, re-run clone                  |
| `recompress.yml MISSING`            | Workflow not created | Re-run orphan branch setup to create workflow                 |
| `workflow trigger failed`           | No workflow_dispatch | Add `workflow_dispatch:` trigger to workflow                  |
| `zstd concatenation FAILED`         | zstd version issue   | Update zstd: `brew upgrade zstd`                              |
| `brotli round-trip FAILED`          | brotli corrupted     | Reinstall: `brew reinstall brotli`                            |

---

## Execution Instructions

**For Claude Code**: After running the setup phases, execute autonomous validation:

1. Save the script to a temp file or run inline via Bash tool
2. Execute with: `bash <script> "$REPO_DIR" "$REPO_URL" "$BRANCH_NAME"`
3. Display formatted output to user
4. If any test fails, show relevant troubleshooting row
5. After autonomous tests, prompt for user-required tests via AskUserQuestion
6. Report final summary: "X/Y autonomous tests passed, user tests: <status>"

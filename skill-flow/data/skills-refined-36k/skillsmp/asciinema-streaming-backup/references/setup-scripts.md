# Setup Scripts

Complete setup and validation scripts for the asciinema streaming backup system.

## preflight-check.sh

Validates all required tools are installed.

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
#!/usr/bin/env bash
# preflight-check.sh - Validates all requirements with self-correction
#
# Usage: preflight-check.sh [--fix]
#   --fix  Attempt to install missing tools via Homebrew

set -euo pipefail

FIX_MODE="${1:-}"
MISSING=()
WARNINGS=()

log() { echo "[preflight] $*"; }
warn() { WARNINGS+=("$*"); }
fail() { MISSING+=("$*"); }

# Check each required tool
check_tool() {
  local tool="$1"
  local install_cmd="${2:-brew install $tool}"

  if command -v "$tool" &>/dev/null; then
    log "$tool: OK ($(command -v "$tool"))"
  else
    fail "$tool"
    log "$tool: MISSING"
    log "  Install: $install_cmd"
  fi
}

log "=== Checking required tools ==="
check_tool "asciinema" "brew install asciinema"
check_tool "zstd" "brew install zstd"
check_tool "brotli" "brew install brotli"
check_tool "git" "xcode-select --install"
check_tool "gh" "brew install gh"

log ""
log "=== Checking optional tools ==="
if command -v fswatch &>/dev/null; then
  log "fswatch: OK (enables real-time monitoring)"
else
  log "fswatch: NOT INSTALLED (optional)"
  log "  Install: brew install fswatch"
fi

# Check asciinema version
if command -v asciinema &>/dev/null; then
  log ""
  log "=== Checking versions ==="
  ASCIINEMA_VERSION=$(asciinema --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
  if [[ -n "$ASCIINEMA_VERSION" ]]; then
    MAJOR="${ASCIINEMA_VERSION%%.*}"
    if (( MAJOR >= 3 )); then
      log "asciinema: v$ASCIINEMA_VERSION (Rust version, recommended)"
    else
      warn "asciinema: v$ASCIINEMA_VERSION (Python version, upgrade recommended)"
      log "  Upgrade: brew upgrade asciinema"
    fi
  fi
fi

# Check gh authentication
if command -v gh &>/dev/null; then
  log ""
  log "=== Checking GitHub CLI auth ==="
  if gh auth status &>/dev/null; then
    log "gh: Authenticated"
  else
    warn "gh: Not authenticated"
    log "  Run: gh auth login"
  fi
fi

# Summary
log ""
log "=== Summary ==="

if [[ ${#MISSING[@]} -gt 0 ]]; then
  log "Missing tools: ${MISSING[*]}"

  if [[ "$FIX_MODE" == "--fix" ]]; then
    log ""
    log "Attempting to install missing tools..."
    brew install "${MISSING[@]}"
    log "Installation complete. Re-run preflight to verify."
  else
    log ""
    log "To install all missing tools:"
    log "  brew install ${MISSING[*]}"
    log ""
    log "Or run: $0 --fix"
    exit 1
  fi
else
  log "All required tools installed"
fi

if [[ ${#WARNINGS[@]} -gt 0 ]]; then
  log ""
  log "Warnings:"
  for w in "${WARNINGS[@]}"; do
    log "  - $w"
  done
fi
PREFLIGHT_EOF
```

## setup-orphan-branch.sh

Creates the orphan branch with GitHub Actions workflow.

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF_2'
#!/usr/bin/env bash
# setup-orphan-branch.sh - Creates gh-recordings orphan branch
#
# Usage: setup-orphan-branch.sh <repo_url>
#   repo_url  SSH or HTTPS URL (e.g., git@github.com:user/repo.git)
#
# Creates:
#   - Orphan branch 'gh-recordings' with separate history
#   - GitHub Actions workflow for brotli recompression
#   - Local clone at ~/asciinema_recordings/<repo-name>/

set -euo pipefail

REPO_URL="${1:?Usage: setup-orphan-branch.sh <repo_url>}"
BRANCH="gh-recordings"
BROTLI_LEVEL="${BROTLI_LEVEL:-9}"

# Extract repo name from URL
REPO_NAME=$(basename "$REPO_URL" .git)
LOCAL_DIR="$HOME/asciinema_recordings/$REPO_NAME"

log() { echo "[setup] $*"; }

# Detect GitHub account from gh auth
detect_github_account() {
  log "Detecting GitHub accounts..."
  ACCOUNTS=$(gh auth status 2>&1 | grep -oE 'Logged in to github.com account [^ ]+' | awk '{print $NF}' || true)

  if [[ -z "$ACCOUNTS" ]]; then
    log "ERROR: No GitHub accounts found. Run 'gh auth login' first."
    exit 1
  fi

  ACTIVE_ACCOUNT=$(gh auth status 2>&1 | grep -A1 'github.com' | grep 'Active account: true' -B1 | head -1 | awk '{print $NF}' || echo "$ACCOUNTS" | head -1)
  log "Active GitHub account: $ACTIVE_ACCOUNT"

  # Check if correct account for this repo
  REPO_OWNER=$(echo "$REPO_URL" | sed -E 's|.*github.com[:/]([^/]+)/.*|\1|')
  if [[ "$ACTIVE_ACCOUNT" != "$REPO_OWNER" ]]; then
    log "Switching to account: $REPO_OWNER"
    if ! gh auth switch --user "$REPO_OWNER" 2>/dev/null; then
      log "WARNING: Could not switch to $REPO_OWNER, using $ACTIVE_ACCOUNT"
    fi
  fi

  SELECTED_ACCOUNT="${REPO_OWNER:-$ACTIVE_ACCOUNT}"
}

# Get SSH key for selected account
get_ssh_key() {
  local account="$1"
  local key_path="$HOME/.ssh/id_ed25519_${account}"

  if [[ -f "$key_path" ]]; then
    echo "$key_path"
  elif [[ -f "$HOME/.ssh/id_ed25519" ]]; then
    echo "$HOME/.ssh/id_ed25519"
  else
    echo ""
  fi
}

detect_github_account
SSH_KEY=$(get_ssh_key "$SELECTED_ACCOUNT")
if [[ -n "$SSH_KEY" ]]; then
  export GIT_SSH_COMMAND="ssh -i $SSH_KEY"
  log "Using SSH key: $SSH_KEY"
fi

log "Repository: $REPO_URL"
log "Branch: $BRANCH"
log "Local directory: $LOCAL_DIR"
log ""

# Check if branch already exists
if git ls-remote --heads "$REPO_URL" "$BRANCH" 2>/dev/null | grep -q "$BRANCH"; then
  log "Orphan branch '$BRANCH' already exists on remote"

  if [[ -d "$LOCAL_DIR" ]]; then
    log "Local clone already exists: $LOCAL_DIR"
    log "Pulling latest..."
    git -C "$LOCAL_DIR" pull
  else
    log "Cloning to: $LOCAL_DIR"
    mkdir -p "$(dirname "$LOCAL_DIR")"
    git clone --single-branch --branch "$BRANCH" --depth 1 "$REPO_URL" "$LOCAL_DIR"
  fi

  log "Setup complete"
  exit 0
fi

log "Creating orphan branch..."

# Create temporary clone for setup
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

git clone --depth 1 "$REPO_URL" "$TEMP_DIR"
cd "$TEMP_DIR"

# Create orphan branch
git checkout --orphan "$BRANCH"
git rm -rf .

# Setup directory structure
mkdir -p .github/workflows chunks archives

# Create GitHub Actions workflow (brotli level embedded at creation time)
cat > .github/workflows/recompress.yml << WORKFLOW_EOF
name: Recompress to Brotli

on:
  push:
    branches: [gh-recordings]
    paths: ['chunks/**/*.zst']
  workflow_dispatch:

jobs:
  recompress:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4

      - name: Install tools
        run: sudo apt-get update && sudo apt-get install -y zstd brotli

      - name: Recompress chunks
        run: |
          if compgen -G "chunks/*.zst" > /dev/null; then
            mkdir -p archives
            ARCHIVE="session_\$(date +%Y%m%d_%H%M%S).cast.br"
            ls -1 chunks/*.zst | sort | xargs cat | zstd -d | brotli -${BROTLI_LEVEL} -o "archives/\$ARCHIVE"
            rm -f chunks/*.zst
            echo "ARCHIVE=\$ARCHIVE" >> \$GITHUB_ENV
          fi

      - name: Commit
        if: env.ARCHIVE != ''
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: archive to brotli (\${{ env.ARCHIVE }})"
          file_pattern: 'archives/*.br chunks/'
WORKFLOW_EOF

# Create placeholder files
cat > chunks/README.md << 'EOF'
# Chunks

Streaming zstd-compressed recording chunks.
Auto-deleted after archival to brotli.
EOF

cat > archives/README.md << 'EOF'
# Archives

Final brotli-compressed recordings.
~300x compression ratio.
EOF

# Create main README
cat > README.md << 'EOF'
# Recording Storage

Orphan branch for asciinema recording backups.
Completely isolated from main codebase history.

## Structure

- `chunks/` - Streaming zstd chunks (temporary)
- `archives/` - Brotli archives (permanent)

## Workflow

1. Local idle-chunker creates zstd chunks
2. Chunks pushed to this branch
3. GitHub Action recompresses to brotli
4. Chunks deleted, archives retained

## Isolation

This is an orphan branch with no shared history.
Git refuses to merge with main: "refusing to merge unrelated histories"
EOF

# Initial commit
git add .
git commit -m "init: recording storage (orphan branch)"

# Push
log "Pushing orphan branch to remote..."
git push -u origin "$BRANCH"

# Clone to local recordings directory
cd -
mkdir -p "$(dirname "$LOCAL_DIR")"
git clone --single-branch --branch "$BRANCH" --depth 1 "$REPO_URL" "$LOCAL_DIR"

# Copy idle-chunker script
cat > "$LOCAL_DIR/idle-chunker.sh" << 'CHUNKER_EOF'
#!/usr/bin/env bash
# idle-chunker.sh - See references/idle-chunker.md for full version
CAST_FILE="${1:?Usage: idle-chunker.sh <cast_file>}"
IDLE_THRESHOLD="${2:-30}"
cd "$(dirname "$0")"
last_pos=0
echo "Monitoring: $CAST_FILE (idle threshold: ${IDLE_THRESHOLD}s)"
while [[ -f "$CAST_FILE" ]] || sleep 2; do
  [[ -f "$CAST_FILE" ]] || continue
  mtime=$(stat -f%m "$CAST_FILE" 2>/dev/null || stat -c%Y "$CAST_FILE")
  idle=$(($(date +%s) - mtime))
  size=$(stat -f%z "$CAST_FILE" 2>/dev/null || stat -c%s "$CAST_FILE")
  if (( idle >= IDLE_THRESHOLD && size > last_pos )); then
    chunk="chunks/chunk_$(date +%Y%m%d_%H%M%S).cast"
    tail -c +$((last_pos + 1)) "$CAST_FILE" > "$chunk"
    zstd -3 --rm "$chunk"
    git add chunks/ && git commit -m "chunk $(date +%H:%M)" && git push
    last_pos=$size
    echo "[$(date +%H:%M:%S)] Created: ${chunk}.zst"
  fi
  sleep 5
done
CHUNKER_EOF
chmod +x "$LOCAL_DIR/idle-chunker.sh"

log ""
log "=== Setup Complete ==="
log "Local directory: $LOCAL_DIR"
log "Idle chunker: $LOCAL_DIR/idle-chunker.sh"
log ""
log "To start recording:"
log "  1. asciinema rec /path/to/session.cast"
log "  2. $LOCAL_DIR/idle-chunker.sh /path/to/session.cast"
PREFLIGHT_EOF_2
```

## validate-system.sh

Complete system validation with self-correction.

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF_3'
#!/usr/bin/env bash
# validate-system.sh - Full system validation
#
# Usage: validate-system.sh <repo_url> [--fix]

set -euo pipefail

REPO_URL="${1:?Usage: validate-system.sh <repo_url> [--fix]}"
FIX_MODE="${2:-}"
REPO_NAME=$(basename "$REPO_URL" .git)
LOCAL_DIR="$HOME/asciinema_recordings/$REPO_NAME"

ERRORS=()
FIXES=()

log() { echo "[validate] $*"; }
error() { ERRORS+=("$*"); log "ERROR: $*"; }
fix() { FIXES+=("$*"); }

log "=== Validating Streaming Backup System ==="
log "Repository: $REPO_URL"
log "Local: $LOCAL_DIR"
log ""

# 1. Check tools
log "--- Tools ---"
for tool in asciinema zstd brotli git gh; do
  if command -v "$tool" &>/dev/null; then
    log "$tool: OK"
  else
    error "$tool: MISSING"
    fix "brew install $tool"
  fi
done

# 2. Check orphan branch exists
log ""
log "--- Remote Branch ---"
if git ls-remote --heads "$REPO_URL" gh-recordings 2>/dev/null | grep -q gh-recordings; then
  log "gh-recordings: EXISTS"
else
  error "gh-recordings: NOT FOUND"
  fix "./setup-orphan-branch.sh $REPO_URL"
fi

# 3. Check local clone
log ""
log "--- Local Clone ---"
if [[ -d "$LOCAL_DIR" ]]; then
  log "Directory: EXISTS"

  # Check it's correct branch
  BRANCH=$(git -C "$LOCAL_DIR" branch --show-current 2>/dev/null || echo "")
  if [[ "$BRANCH" == "gh-recordings" ]]; then
    log "Branch: OK (gh-recordings)"
  else
    error "Branch: WRONG ($BRANCH)"
    fix "cd $LOCAL_DIR && git checkout gh-recordings"
  fi

  # Check workflow exists
  if [[ -f "$LOCAL_DIR/.github/workflows/recompress.yml" ]]; then
    log "Workflow: EXISTS"
  else
    error "Workflow: MISSING"
    fix "Regenerate workflow"
  fi

  # Check directories
  [[ -d "$LOCAL_DIR/chunks" ]] && log "chunks/: EXISTS" || error "chunks/: MISSING"
  [[ -d "$LOCAL_DIR/archives" ]] && log "archives/: EXISTS" || error "archives/: MISSING"

  # Check idle-chunker
  if [[ -x "$LOCAL_DIR/idle-chunker.sh" ]]; then
    log "idle-chunker.sh: EXISTS"
  else
    error "idle-chunker.sh: MISSING"
  fi
else
  error "Local directory: NOT FOUND"
  fix "git clone --single-branch --branch gh-recordings --depth 1 $REPO_URL $LOCAL_DIR"
fi

# 4. Test compression
log ""
log "--- Compression Test ---"
TEST_DATA="test-$(date +%s)"
if echo "$TEST_DATA" | zstd -3 | zstd -d | grep -q "$TEST_DATA"; then
  log "zstd round-trip: OK"
else
  error "zstd round-trip: FAILED"
fi

if echo "$TEST_DATA" | brotli | brotli -d | grep -q "$TEST_DATA"; then
  log "brotli round-trip: OK"
else
  error "brotli round-trip: FAILED"
fi

# 5. Test zstd concatenation
log ""
log "--- Concatenation Test ---"
TMP=$(mktemp -d)
echo "chunk1" | zstd -3 > "$TMP/a.zst"
echo "chunk2" | zstd -3 > "$TMP/b.zst"
cat "$TMP/a.zst" "$TMP/b.zst" > "$TMP/combined.zst"
RESULT=$(zstd -d -c "$TMP/combined.zst")
rm -rf "$TMP"

if [[ "$RESULT" == $'chunk1\nchunk2' ]]; then
  log "zstd concatenation: OK"
else
  error "zstd concatenation: FAILED"
fi

# Summary
log ""
log "=== Summary ==="

if [[ ${#ERRORS[@]} -eq 0 ]]; then
  log "All checks passed"
  exit 0
fi

log "Errors found: ${#ERRORS[@]}"
for e in "${ERRORS[@]}"; do
  log "  - $e"
done

if [[ ${#FIXES[@]} -gt 0 ]]; then
  log ""
  log "Suggested fixes:"
  for f in "${FIXES[@]}"; do
    log "  $f"
  done
fi

exit 1
PREFLIGHT_EOF_3
```

## test-workflow.sh

Test the complete workflow end-to-end.

```bash
/usr/bin/env bash << 'VALIDATE_EOF'
#!/usr/bin/env bash
# test-workflow.sh - End-to-end workflow test
#
# Usage: test-workflow.sh <local_recordings_dir>
#
# Creates a test recording, generates chunks, and verifies round-trip

set -euo pipefail

LOCAL_DIR="${1:?Usage: test-workflow.sh <local_recordings_dir>}"

log() { echo "[test] $*"; }

log "=== Testing Streaming Backup Workflow ==="
log "Directory: $LOCAL_DIR"

# Create test .cast file
TEST_CAST=$(mktemp).cast
log ""
log "Creating test recording: $TEST_CAST"

cat > "$TEST_CAST" << 'CAST_EOF'
{"version": 2, "width": 80, "height": 24, "timestamp": 1234567890}
[0.1, "o", "$ echo hello\r\n"]
[0.2, "o", "hello\r\n"]
[0.3, "o", "$ echo world\r\n"]
[0.4, "o", "world\r\n"]
CAST_EOF

log "Test recording created ($(wc -l < "$TEST_CAST") lines)"

# Simulate chunking
log ""
log "Creating test chunks..."
cd "$LOCAL_DIR"
mkdir -p chunks

# Chunk 1: header + first command
head -3 "$TEST_CAST" > chunks/test_001.cast
zstd -3 --rm chunks/test_001.cast
log "Created: chunks/test_001.cast.zst"

# Chunk 2: remaining lines
tail -n +4 "$TEST_CAST" > chunks/test_002.cast
zstd -3 --rm chunks/test_002.cast
log "Created: chunks/test_002.cast.zst"

# Test concatenation
log ""
log "Testing concatenation..."
cat chunks/test_*.zst > /tmp/test_combined.zst
zstd -d /tmp/test_combined.zst -o /tmp/test_combined.cast

# Verify content
if diff -q "$TEST_CAST" /tmp/test_combined.cast &>/dev/null; then
  log "Concatenation: PASSED (content matches)"
else
  log "Concatenation: FAILED (content differs)"
  diff "$TEST_CAST" /tmp/test_combined.cast
  exit 1
fi

# Test brotli recompression
log ""
log "Testing brotli recompression..."
brotli -9 /tmp/test_combined.cast -o /tmp/test_archive.cast.br
brotli -d /tmp/test_archive.cast.br -o /tmp/test_final.cast

if diff -q "$TEST_CAST" /tmp/test_final.cast &>/dev/null; then
  log "Brotli round-trip: PASSED"
else
  log "Brotli round-trip: FAILED"
  exit 1
fi

# Size comparison
ORIG_SIZE=$(wc -c < "$TEST_CAST")
ZSTD_SIZE=$(cat chunks/test_*.zst | wc -c)
BR_SIZE=$(wc -c < /tmp/test_archive.cast.br)

log ""
log "=== Size Comparison ==="
log "Original: $ORIG_SIZE bytes"
log "zstd chunks: $ZSTD_SIZE bytes ($(echo "scale=1; $ORIG_SIZE / $ZSTD_SIZE" | bc)x)"
log "brotli: $BR_SIZE bytes ($(echo "scale=1; $ORIG_SIZE / $BR_SIZE" | bc)x)"

# Cleanup test files
rm -f "$TEST_CAST" /tmp/test_*.cast /tmp/test_*.zst /tmp/test_*.br
rm -f chunks/test_*.zst

log ""
log "=== All Tests Passed ==="
VALIDATE_EOF
```

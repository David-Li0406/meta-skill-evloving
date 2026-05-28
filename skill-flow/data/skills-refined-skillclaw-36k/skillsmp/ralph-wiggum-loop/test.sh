#!/bin/bash
# gumloop test suite
# Run: ./test.sh

set -uo pipefail
# Note: not using set -e because we need to handle expected failures

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

GUMLOOP="$(cd "$(dirname "$0")" && pwd)/gumloop"
TEST_DIR="/tmp/gumloop-test-$$"
PASSED=0
FAILED=0

# Cleanup on exit
cleanup() {
    rm -rf "$TEST_DIR" 2>/dev/null || true
    rm -f /tmp/mock-agent-* 2>/dev/null || true
}
trap cleanup EXIT

# Test helpers
pass() {
    echo -e "  ${GREEN}✓${NC} $1"
    PASSED=$((PASSED + 1))
}

fail() {
    echo -e "  ${RED}✗${NC} $1"
    echo -e "    ${YELLOW}$2${NC}"
    FAILED=$((FAILED + 1))
}

section() {
    echo ""
    echo -e "${YELLOW}▸ $1${NC}"
}

# Setup test directory
setup_test_repo() {
    rm -rf "$TEST_DIR"
    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR"
    git init -q
    git config user.email "test@test.com"
    git config user.name "Test"
    # Create initial commit so HEAD exists
    echo "init" > .gitkeep
    git add .gitkeep
    git commit -q -m "Initial commit"
}

# ============================================================================
# TESTS
# ============================================================================

section "Basic Commands"

# --version
if "$GUMLOOP" --version 2>&1 | grep -q "gumloop"; then
    pass "--version shows version"
else
    fail "--version shows version" "Did not contain 'gumloop'"
fi

# --help
if "$GUMLOOP" --help 2>&1 | grep -q "OPTIONS:"; then
    pass "--help shows help"
else
    fail "--help shows help" "Did not contain 'OPTIONS:'"
fi

# --help shows new options
HELP_OUTPUT=$("$GUMLOOP" --help 2>&1)
for opt in "stuck-threshold" "verify" "init" "recover"; do
    if echo "$HELP_OUTPUT" | grep -q -- "--$opt"; then
        pass "--help includes --$opt"
    else
        fail "--help includes --$opt" "Option not found in help"
    fi
done


section "Safety Checks"

# Refuses root
ROOT_OUTPUT=$(cd / && "$GUMLOOP" -p "test" 2>&1) || true
if echo "$ROOT_OUTPUT" | grep -q "SAFETY"; then
    pass "Refuses dangerous paths (/)"
else
    fail "Refuses dangerous paths (/)" "Did not refuse: $ROOT_OUTPUT"
fi

# Refuses home
HOME_OUTPUT=$(cd "$HOME" && "$GUMLOOP" -p "test" 2>&1) || true
if echo "$HOME_OUTPUT" | grep -q "SAFETY"; then
    pass "Refuses dangerous paths (~)"
else
    fail "Refuses dangerous paths (~)" "Did not refuse: $HOME_OUTPUT"
fi

# Requires git
NO_GIT_DIR="/tmp/gumloop-no-git-$$"
mkdir -p "$NO_GIT_DIR"
NO_GIT_OUTPUT=$(cd "$NO_GIT_DIR" && "$GUMLOOP" -p "test" 2>&1) || true
if echo "$NO_GIT_OUTPUT" | grep -q "Not in a git repository"; then
    pass "Requires git repository"
else
    fail "Requires git repository" "Did not require git: $NO_GIT_OUTPUT"
fi
rm -rf "$NO_GIT_DIR"


section "--init Command"

setup_test_repo

# Creates PROMPT.md
INIT_OUTPUT=$("$GUMLOOP" --init 2>&1) || true
if echo "$INIT_OUTPUT" | grep -q "Created PROMPT.md"; then
    pass "--init creates PROMPT.md"
else
    fail "--init creates PROMPT.md" "Output: $INIT_OUTPUT"
fi

# File has correct content
if grep -q "ONE task per session" PROMPT.md 2>/dev/null; then
    pass "--init template has correct content"
else
    fail "--init template has correct content" "Content missing"
fi

# Refuses to overwrite
OVERWRITE_OUTPUT=$("$GUMLOOP" --init 2>&1) || true
if echo "$OVERWRITE_OUTPUT" | grep -q "already exists"; then
    pass "--init refuses to overwrite existing file"
else
    fail "--init refuses to overwrite existing file" "Output: $OVERWRITE_OUTPUT"
fi

# Custom filename
CUSTOM_OUTPUT=$("$GUMLOOP" --init CUSTOM.md 2>&1) || true
if echo "$CUSTOM_OUTPUT" | grep -q "Created CUSTOM.md"; then
    pass "--init CUSTOM.md creates custom file"
else
    fail "--init CUSTOM.md creates custom file" "Output: $CUSTOM_OUTPUT"
fi


section "--recover Command"

setup_test_repo

# No changes = reports no changes
RECOVER_CLEAN=$(echo "n" | "$GUMLOOP" --recover 2>&1) || true
if echo "$RECOVER_CLEAN" | grep -q "No uncommitted changes"; then
    pass "--recover with no changes reports clean state"
else
    fail "--recover with no changes reports clean state" "Output: $RECOVER_CLEAN"
fi

# With changes = shows warning, pipe "n" to decline
echo "dirty" > dirty.txt
RECOVER_DIRTY=$(echo "n" | "$GUMLOOP" --recover 2>&1) || true
if echo "$RECOVER_DIRTY" | grep -q "RECOVERY MODE"; then
    pass "--recover shows recovery mode warning"
else
    fail "--recover shows recovery mode warning" "Output: $RECOVER_DIRTY"
fi


section "Argument Parsing"

setup_test_repo

# No prompt = error
NO_PROMPT_OUTPUT=$("$GUMLOOP" --choo-choo 2>&1) || true
if echo "$NO_PROMPT_OUTPUT" | grep -q "No prompt provided"; then
    pass "Requires prompt or prompt file"
else
    fail "Requires prompt or prompt file" "Output: $NO_PROMPT_OUTPUT"
fi

# --cli requires value
CLI_OUTPUT=$("$GUMLOOP" --cli 2>&1) || true
if echo "$CLI_OUTPUT" | grep -q "requires a value"; then
    pass "--cli requires a value"
else
    fail "--cli requires a value" "Output: $CLI_OUTPUT"
fi

# --stuck-threshold requires value
STUCK_OUTPUT=$("$GUMLOOP" --stuck-threshold 2>&1) || true
if echo "$STUCK_OUTPUT" | grep -q "requires"; then
    pass "--stuck-threshold requires a value"
else
    fail "--stuck-threshold requires a value" "Output: $STUCK_OUTPUT"
fi

# --verify requires value
VERIFY_OUTPUT=$("$GUMLOOP" --verify 2>&1) || true
if echo "$VERIFY_OUTPUT" | grep -q "requires"; then
    pass "--verify requires a value"
else
    fail "--verify requires a value" "Output: $VERIFY_OUTPUT"
fi


section "Mock Agent Tests"

setup_test_repo

# Create mock agent that makes changes but doesn't commit
cat > /tmp/mock-agent-nocommit << 'EOF'
#!/bin/bash
echo "change $(date +%s)" >> changes.txt
EOF
chmod +x /tmp/mock-agent-nocommit

# Create mock agent that commits (always creates unique changes)
cat > /tmp/mock-agent-commits << 'EOF'
#!/bin/bash
# Always create a new unique file to ensure there are always changes
echo "change $(date +%s)-$RANDOM" > "file-$(date +%s)-$RANDOM.txt"
git add -A
git commit -q -m "Auto commit $(date +%s)"
EOF
chmod +x /tmp/mock-agent-commits

# Create mock agent that does nothing (for completion test)
cat > /tmp/mock-agent-noop << 'EOF'
#!/bin/bash
echo "Nothing to do"
EOF
chmod +x /tmp/mock-agent-noop

# Test stuck detection
setup_test_repo
STUCK_OUTPUT=$("$GUMLOOP" --cli /tmp/mock-agent-nocommit --choo-choo --stuck-threshold 2 -p "test" 2>&1 || true)
if echo "$STUCK_OUTPUT" | grep -q -i "stuck"; then
    pass "Stuck detection triggers after threshold"
else
    fail "Stuck detection triggers after threshold" "Did not detect stuck: $STUCK_OUTPUT"
fi

# Test completion detection (no changes = done)
setup_test_repo
COMPLETE_OUTPUT=$("$GUMLOOP" --cli /tmp/mock-agent-noop --choo-choo -p "test" 2>&1 || true)
if echo "$COMPLETE_OUTPUT" | grep -q "No changes detected"; then
    pass "Completion detection (no changes = done)"
else
    fail "Completion detection (no changes = done)" "Did not detect completion"
fi

# Test max iterations (agent must leave uncommitted changes to continue looping)
setup_test_repo
cat > /tmp/mock-agent-maxtest << 'EOF'
#!/bin/bash
# Commit something AND leave uncommitted changes
echo "committed $(date +%s)" > committed.txt
git add committed.txt
git commit -q -m "Commit"
echo "uncommitted $(date +%s)" > uncommitted.txt
EOF
chmod +x /tmp/mock-agent-maxtest
MAX_OUTPUT=$("$GUMLOOP" --cli /tmp/mock-agent-maxtest --choo-choo 2 -p "test" 2>&1 || true)
if echo "$MAX_OUTPUT" | grep -q "Max iterations"; then
    pass "Max iterations limit works"
else
    fail "Max iterations limit works" "Output did not contain 'Max iterations'"
fi

# Test single run mode (no --choo-choo)
setup_test_repo
SINGLE_OUTPUT=$("$GUMLOOP" --cli /tmp/mock-agent-commits -p "test" 2>&1 || true)
if echo "$SINGLE_OUTPUT" | grep -q "ITERATION 1" && ! echo "$SINGLE_OUTPUT" | grep -q "ITERATION 2"; then
    pass "Single run mode (no --choo-choo) runs once"
else
    fail "Single run mode runs once" "Ran more than once"
fi

# Test --verify flag runs
setup_test_repo
VERIFY_OUTPUT=$("$GUMLOOP" --cli /tmp/mock-agent-noop --verify "echo VERIFY_RAN" -p "test" 2>&1 || true)
if echo "$VERIFY_OUTPUT" | grep -q "Verifying"; then
    pass "--verify command is executed"
else
    fail "--verify command is executed" "Verify not run"
fi


section "Exit Reason Reporting"

setup_test_repo
REPORT_OUTPUT=$("$GUMLOOP" --cli /tmp/mock-agent-noop -p "test" 2>&1 || true)
if echo "$REPORT_OUTPUT" | grep -q "Exit:"; then
    pass "Exit reason is reported"
else
    fail "Exit reason is reported" "No exit reason in output"
fi


# ============================================================================
# SUMMARY
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  Tests: $((PASSED + FAILED))  ${GREEN}Passed: $PASSED${NC}  ${RED}Failed: $FAILED${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAILED -gt 0 ]; then
    exit 1
fi

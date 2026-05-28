#!/usr/bin/env bats
# Self-Evolving Agent - Checkpoint Tests
# Tests for CP0-CP6.5 checkpoint documentation and scripts

setup() {
    PROJECT_ROOT="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
    CHECKPOINTS_DIR="$PROJECT_ROOT/skills/02-checkpoints/_base"
    SCRIPTS_DIR="$PROJECT_ROOT/scripts"
}

# ============================================================
# Checkpoint Documentation Tests
# ============================================================

@test "CP0 (North Star) exists and has required sections" {
    local file="$CHECKPOINTS_DIR/cp0-north-star.md"
    [ -f "$file" ]

    # Check for required sections
    grep -q "願景" "$file" || grep -q "vision" "$file"
    grep -q "完成標準" "$file" || grep -q "completion" "$file"
}

@test "CP0.5 (Worktree Setup) exists" {
    [ -f "$CHECKPOINTS_DIR/cp0.5-worktree-setup.md" ]
}

@test "CP1 (Memory Search) exists and has search instructions" {
    local file="$CHECKPOINTS_DIR/cp1-memory-search.md"
    [ -f "$file" ]

    # Check for memory search content
    grep -qi "memory\|搜尋\|search" "$file"
}

@test "CP1.5 (Consistency Check) exists" {
    [ -f "$CHECKPOINTS_DIR/cp1.5-consistency-check.md" ]
}

@test "CP2 (Build Test) exists and mentions verification" {
    local file="$CHECKPOINTS_DIR/cp2-build-test.md"
    [ -f "$file" ]

    # Check for test/build content
    grep -qi "test\|build\|測試\|編譯" "$file"
}

@test "CP3 (Milestone Confirm) exists" {
    [ -f "$CHECKPOINTS_DIR/cp3-milestone-confirm.md" ]
}

@test "CP3.5 (Memory Sync) exists and mentions index" {
    local file="$CHECKPOINTS_DIR/cp3.5-memory-sync.md"
    [ -f "$file" ]

    # Check for index sync content
    grep -qi "index\|sync\|同步" "$file"
}

@test "CP4 (Emergence Check) exists" {
    [ -f "$CHECKPOINTS_DIR/cp4-emergence-check.md" ]
}

@test "CP5 (Failure Postmortem) exists and has diagnostic content" {
    local file="$CHECKPOINTS_DIR/cp5-failure-postmortem.md"
    [ -f "$file" ]

    # Check for failure analysis content
    grep -qi "失敗\|failure\|診斷\|diagnostic" "$file"
}

@test "CP6 (Project Health Check) exists" {
    [ -f "$CHECKPOINTS_DIR/cp6-project-health-check.md" ]
}

@test "CP6.5 (Worktree Completion) exists" {
    [ -f "$CHECKPOINTS_DIR/cp6.5-worktree-completion.md" ]
}

@test "All checkpoints have valid markdown format" {
    for file in "$CHECKPOINTS_DIR"/cp*.md; do
        # Check file is not empty
        [ -s "$file" ]

        # Check has at least one heading
        grep -q "^#" "$file"
    done
}

# ============================================================
# Checkpoint Script Tests
# ============================================================

@test "CP1 script has valid bash syntax" {
    [ -f "$SCRIPTS_DIR/cp1-memory-search.sh" ]
    bash -n "$SCRIPTS_DIR/cp1-memory-search.sh"
}

@test "CP1.5 script has valid bash syntax" {
    [ -f "$SCRIPTS_DIR/cp1.5-consistency-check.sh" ]
    bash -n "$SCRIPTS_DIR/cp1.5-consistency-check.sh"
}

@test "CP2 script has valid bash syntax" {
    [ -f "$SCRIPTS_DIR/cp2-verify-build.sh" ]
    bash -n "$SCRIPTS_DIR/cp2-verify-build.sh"
}

@test "CP3.5 script has valid bash syntax" {
    [ -f "$SCRIPTS_DIR/cp3.5-memory-sync.sh" ]
    bash -n "$SCRIPTS_DIR/cp3.5-memory-sync.sh"
}

@test "All checkpoint scripts are executable" {
    for script in "$SCRIPTS_DIR"/cp*.sh; do
        [ -x "$script" ]
    done
}

# ============================================================
# Checkpoint README Tests
# ============================================================

@test "Checkpoints README exists and lists all checkpoints" {
    local readme="$PROJECT_ROOT/skills/02-checkpoints/README.md"
    [ -f "$readme" ]

    # Check all checkpoints are mentioned
    grep -q "CP0" "$readme"
    grep -q "CP1" "$readme"
    grep -q "CP2" "$readme"
    grep -q "CP3" "$readme"
    grep -q "CP5" "$readme"
    grep -q "CP6" "$readme"
}

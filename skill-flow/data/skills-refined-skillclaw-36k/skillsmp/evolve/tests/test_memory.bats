#!/usr/bin/env bats
# Self-Evolving Agent - Memory System Tests
# Comprehensive tests for Git-based memory system

setup() {
    PROJECT_ROOT="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
    MEMORY_DIR="$PROJECT_ROOT/.claude/memory"
    MEMORY_SKILLS="$PROJECT_ROOT/skills/03-memory/_base"
}

# ============================================================
# Memory Directory Structure
# ============================================================

@test "Memory root directory exists" {
    [ -d "$MEMORY_DIR" ]
}

@test "Memory index.md exists" {
    [ -f "$MEMORY_DIR/index.md" ]
}

@test "Memory learnings directory exists" {
    [ -d "$MEMORY_DIR/learnings" ]
}

@test "Memory failures directory exists" {
    [ -d "$MEMORY_DIR/failures" ]
}

@test "Memory decisions directory exists" {
    [ -d "$MEMORY_DIR/decisions" ]
}

@test "Memory patterns directory exists" {
    [ -d "$MEMORY_DIR/patterns" ]
}

@test "Memory plans directory exists" {
    [ -d "$MEMORY_DIR/plans" ]
}

# ============================================================
# Memory Index Format
# ============================================================

@test "Memory index has LEARNINGS markers" {
    grep -q "LEARNINGS_START" "$MEMORY_DIR/index.md"
    grep -q "LEARNINGS_END" "$MEMORY_DIR/index.md"
}

@test "Memory index has FAILURES markers" {
    grep -q "FAILURES_START" "$MEMORY_DIR/index.md"
    grep -q "FAILURES_END" "$MEMORY_DIR/index.md"
}

@test "Memory index has TAGS markers" {
    grep -q "TAGS_START" "$MEMORY_DIR/index.md"
    grep -q "TAGS_END" "$MEMORY_DIR/index.md"
}

@test "Memory index has proper markdown structure" {
    # Should have at least one heading
    grep -q "^#" "$MEMORY_DIR/index.md"
}

# ============================================================
# Learning Files Format
# ============================================================

@test "Learning files have valid frontmatter" {
    local count=0
    local valid=0

    for file in "$MEMORY_DIR/learnings"/*.md; do
        if [[ -f "$file" && "$(basename "$file")" != ".gitkeep" ]]; then
            ((count++))
            if head -1 "$file" | grep -q "^---$"; then
                if grep -q "^date:" "$file" && grep -q "^tags:" "$file"; then
                    ((valid++))
                fi
            fi
        fi
    done

    # All files should be valid (or no files exist)
    [ "$count" -eq 0 ] || [ "$count" -eq "$valid" ]
}

@test "Learning files follow naming convention (YYYY-MM-DD-*)" {
    for file in "$MEMORY_DIR/learnings"/*.md; do
        if [[ -f "$file" && "$(basename "$file")" != ".gitkeep" ]]; then
            basename "$file" | grep -qE "^[0-9]{4}-[0-9]{2}-[0-9]{2}-"
        fi
    done
}

# ============================================================
# Failure Files Format
# ============================================================

@test "Failure files have valid frontmatter" {
    local count=0
    local valid=0

    for file in "$MEMORY_DIR/failures"/*.md; do
        if [[ -f "$file" && "$(basename "$file")" != ".gitkeep" ]]; then
            ((count++))
            if head -1 "$file" | grep -q "^---$"; then
                ((valid++))
            fi
        fi
    done

    [ "$count" -eq 0 ] || [ "$count" -eq "$valid" ]
}

# ============================================================
# Memory Skills Documentation
# ============================================================

@test "Memory operations.md exists" {
    [ -f "$MEMORY_SKILLS/operations.md" ]
}

@test "Memory operations has CRUD sections" {
    local file="$MEMORY_SKILLS/operations.md"
    [ -f "$file" ]

    # Check for operation types
    grep -qi "create\|新增\|建立" "$file"
    grep -qi "read\|search\|搜尋\|查詢" "$file"
}

@test "Memory README exists" {
    [ -f "$PROJECT_ROOT/skills/03-memory/README.md" ]
}

# ============================================================
# Memory Script Tests
# ============================================================

@test "validate-memory.sh script exists and is executable" {
    [ -x "$PROJECT_ROOT/scripts/validate-memory.sh" ]
}

@test "validate-memory.sh has valid syntax" {
    bash -n "$PROJECT_ROOT/scripts/validate-memory.sh"
}

@test "cp3.5-memory-sync.sh exists and is executable" {
    [ -x "$PROJECT_ROOT/scripts/cp3.5-memory-sync.sh" ]
}

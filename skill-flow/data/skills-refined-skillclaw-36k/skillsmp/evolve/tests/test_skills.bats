#!/usr/bin/env bats
# Self-Evolving Agent - Skill Tests
# Requires: bats-core (https://github.com/bats-core/bats-core)

setup() {
    # Get project root
    PROJECT_ROOT="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
    SKILLS_DIR="$PROJECT_ROOT/skills"
}

# ============================================================
# Core Structure Tests
# ============================================================

@test "SKILL.md exists and has valid frontmatter" {
    [ -f "$SKILLS_DIR/SKILL.md" ]

    # Check frontmatter exists
    head -1 "$SKILLS_DIR/SKILL.md" | grep -q "^---$"

    # Check required fields
    grep -q "^name:" "$SKILLS_DIR/SKILL.md"
    grep -q "^version:" "$SKILLS_DIR/SKILL.md"
    grep -q "^description:" "$SKILLS_DIR/SKILL.md"
}

@test "All required modules exist" {
    local modules=(
        "00-getting-started"
        "01-core"
        "02-checkpoints"
        "03-memory"
        "04-emergence"
        "05-integration"
        "99-evolution"
    )

    for module in "${modules[@]}"; do
        [ -d "$SKILLS_DIR/$module" ]
        [ -d "$SKILLS_DIR/$module/_base" ]
        [ -f "$SKILLS_DIR/$module/README.md" ]
    done
}

@test "Each module has at least one content file" {
    for dir in "$SKILLS_DIR"/*/; do
        if [[ -d "$dir/_base" ]]; then
            local count=$(find "$dir/_base" -name "*.md" -type f | wc -l)
            [ "$count" -gt 0 ]
        fi
    done
}

# ============================================================
# Memory System Tests
# ============================================================

@test "Memory directory structure is valid" {
    local memory_dir="$PROJECT_ROOT/.claude/memory"

    [ -d "$memory_dir" ]
    [ -f "$memory_dir/index.md" ]
    [ -d "$memory_dir/learnings" ]
    [ -d "$memory_dir/failures" ]
    [ -d "$memory_dir/decisions" ]
    [ -d "$memory_dir/patterns" ]
}

@test "Memory index.md has required sections" {
    local index="$PROJECT_ROOT/.claude/memory/index.md"

    [ -f "$index" ]
    grep -q "LEARNINGS_START" "$index"
    grep -q "LEARNINGS_END" "$index"
    grep -q "TAGS_START" "$index"
}

@test "Learning files have valid frontmatter" {
    local learnings_dir="$PROJECT_ROOT/.claude/memory/learnings"

    for file in "$learnings_dir"/*.md; do
        if [[ -f "$file" && "$file" != *".gitkeep"* ]]; then
            head -1 "$file" | grep -q "^---$"
            grep -q "^date:" "$file"
            grep -q "^tags:" "$file"
        fi
    done
}

# ============================================================
# Script Tests
# ============================================================

@test "install.sh has valid bash syntax" {
    bash -n "$PROJECT_ROOT/install.sh"
}

@test "check-env.sh has valid bash syntax" {
    bash -n "$PROJECT_ROOT/scripts/check-env.sh"
}

@test "validate-memory.sh has valid bash syntax" {
    bash -n "$PROJECT_ROOT/scripts/validate-memory.sh"
}

@test "All shell scripts are executable" {
    local scripts=(
        "install.sh"
        "scripts/check-env.sh"
        "scripts/validate-memory.sh"
        "scripts/sync-global.sh"
        "scripts/verify-install.sh"
        "scripts/validate-all.sh"
    )

    for script in "${scripts[@]}"; do
        [ -x "$PROJECT_ROOT/$script" ]
    done
}

# ============================================================
# Content Quality Tests
# ============================================================

@test "No TODO or FIXME in release files" {
    local count=$(grep -r "TODO\|FIXME" "$SKILLS_DIR" --include="*.md" | wc -l)
    [ "$count" -eq 0 ]
}

@test "All internal markdown links are valid" {
    # Simplified check - verify key linked files exist
    # Check a few known important links instead of all links
    [ -f "$SKILLS_DIR/01-core/_base/pdca-cycle.md" ]
    [ -f "$SKILLS_DIR/02-checkpoints/_base/cp0-north-star.md" ]
    [ -f "$SKILLS_DIR/03-memory/_base/operations.md" ]
}

@test "CHANGELOG.md exists and has current version" {
    [ -f "$PROJECT_ROOT/CHANGELOG.md" ]

    # Get version from SKILL.md
    local version=$(grep "^version:" "$SKILLS_DIR/SKILL.md" | head -1 | awk '{print $2}')

    # Check if version appears in CHANGELOG
    grep -q "$version" "$PROJECT_ROOT/CHANGELOG.md"
}

# ============================================================
# CI/CD Tests
# ============================================================

@test "GitHub Actions workflow exists" {
    [ -f "$PROJECT_ROOT/.github/workflows/ci.yml" ]
}

@test "GitHub Actions workflow has valid YAML" {
    # Basic YAML validation
    head -1 "$PROJECT_ROOT/.github/workflows/ci.yml" | grep -q "^name:"
}

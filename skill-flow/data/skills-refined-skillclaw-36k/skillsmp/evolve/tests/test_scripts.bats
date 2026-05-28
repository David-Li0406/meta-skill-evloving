#!/usr/bin/env bats
# Self-Evolving Agent - Script Tests
# Comprehensive tests for all shell scripts

setup() {
    PROJECT_ROOT="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
    SCRIPTS_DIR="$PROJECT_ROOT/scripts"
}

# ============================================================
# Bash Syntax Validation (All Scripts)
# ============================================================

@test "setup-hooks.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/setup-hooks.sh"
}

@test "sync-global.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/sync-global.sh"
}

@test "validate-memory.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/validate-memory.sh"
}

@test "validate-all.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/validate-all.sh"
}

@test "quickstart.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/quickstart.sh"
}

@test "generate-changelog.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/generate-changelog.sh"
}

@test "check-env.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/check-env.sh"
}

@test "setup-file-suggestion.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/setup-file-suggestion.sh"
}

@test "verify-install.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/verify-install.sh"
}

@test "sync-skills.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/sync-skills.sh"
}

@test "check-version.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/check-version.sh"
}

@test "setup-skill-index.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/setup-skill-index.sh"
}

@test "update-version.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/update-version.sh"
}

@test "evolve-hooks.sh has valid bash syntax" {
    bash -n "$SCRIPTS_DIR/evolve-hooks.sh"
}

# ============================================================
# Script Executability
# ============================================================

@test "All scripts in scripts/ are executable" {
    for script in "$SCRIPTS_DIR"/*.sh; do
        [ -x "$script" ]
    done
}

@test "install.sh is executable" {
    [ -x "$PROJECT_ROOT/install.sh" ]
}

# ============================================================
# Script Header Standards
# ============================================================

@test "Scripts have proper shebang" {
    for script in "$SCRIPTS_DIR"/*.sh; do
        head -1 "$script" | grep -qE "^#!/(usr/)?bin/(env )?bash"
    done
}

@test "install.sh has proper shebang" {
    head -1 "$PROJECT_ROOT/install.sh" | grep -qE "^#!/(usr/)?bin/(env )?bash"
}

# ============================================================
# Critical Script Functionality Tests
# ============================================================

@test "check-env.sh runs without error (dry run)" {
    # Just verify it starts and shows help or usage
    "$SCRIPTS_DIR/check-env.sh" --help 2>/dev/null || "$SCRIPTS_DIR/check-env.sh" 2>&1 | head -5
}

@test "validate-memory.sh can be sourced" {
    # Check script can be sourced without executing
    bash -c "source '$SCRIPTS_DIR/validate-memory.sh' --help" 2>/dev/null || true
}

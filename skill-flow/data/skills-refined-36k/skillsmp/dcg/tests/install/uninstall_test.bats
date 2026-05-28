#!/usr/bin/env bats
# Unit tests for uninstall.sh
#
# Tests:
# - Agent hook removal (Claude Code, Gemini CLI, Aider)
# - Binary removal
# - Configuration and data removal
# - Confirmation prompt behavior

load test_helper

setup() {
    setup_isolated_home
    setup_test_log "$BATS_TEST_NAME"

    # Source uninstall.sh functions
    UNINSTALL_SCRIPT="$PROJECT_ROOT/uninstall.sh"

    # Create mock dcg binary
    mkdir -p "$HOME/.local/bin"
    cat > "$HOME/.local/bin/dcg" << 'MOCKEOF'
#!/bin/bash
echo "dcg 1.0.0"
MOCKEOF
    chmod +x "$HOME/.local/bin/dcg"
    export PATH="$HOME/.local/bin:$PATH"
}

teardown() {
    log_test "=== Test completed: $BATS_TEST_NAME (status: $status) ==="
    teardown_isolated_home
}

# ============================================================================
# Claude Code Uninstall Tests
# ============================================================================

@test "uninstall: removes dcg hook from Claude Code settings" {
    log_test "Testing Claude Code hook removal..."

    # Skip if python3 not available
    command -v python3 &>/dev/null || skip "python3 not available"

    mkdir -p "$HOME/.claude"
    cat > "$HOME/.claude/settings.json" << 'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "/path/to/dcg"}
        ]
      }
    ]
  }
}
EOF

    log_test "Before: $(cat "$HOME/.claude/settings.json")"

    # Run uninstall with --yes to skip confirmation
    "$UNINSTALL_SCRIPT" --yes --quiet

    log_test "After: $(cat "$HOME/.claude/settings.json" 2>/dev/null || echo 'N/A')"

    # dcg hook should be removed
    ! grep -q '"command".*dcg' "$HOME/.claude/settings.json"
}

@test "uninstall: preserves other hooks in Claude Code settings" {
    log_test "Testing preservation of other Claude Code hooks..."

    # Skip if python3 not available
    command -v python3 &>/dev/null || skip "python3 not available"

    mkdir -p "$HOME/.claude"
    cat > "$HOME/.claude/settings.json" << 'EOF'
{
  "theme": "dark",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "/path/to/dcg"},
          {"type": "command", "command": "/path/to/other-hook"}
        ]
      },
      {
        "matcher": "Read",
        "hooks": [{"type": "command", "command": "/path/to/read-hook"}]
      }
    ]
  }
}
EOF

    "$UNINSTALL_SCRIPT" --yes --quiet

    log_test "After: $(cat "$HOME/.claude/settings.json")"

    # Other hooks should remain
    grep -q "other-hook" "$HOME/.claude/settings.json"
    grep -q "read-hook" "$HOME/.claude/settings.json"
    grep -q "theme" "$HOME/.claude/settings.json"
}

# ============================================================================
# Gemini CLI Uninstall Tests
# ============================================================================

@test "uninstall: removes dcg hook from Gemini CLI settings" {
    log_test "Testing Gemini CLI hook removal..."

    # Skip if python3 not available
    command -v python3 &>/dev/null || skip "python3 not available"

    mkdir -p "$HOME/.gemini"
    cat > "$HOME/.gemini/settings.json" << 'EOF'
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "run_shell_command",
        "hooks": [
          {"name": "dcg", "type": "command", "command": "/path/to/dcg"}
        ]
      }
    ]
  }
}
EOF

    "$UNINSTALL_SCRIPT" --yes --quiet

    log_test "After: $(cat "$HOME/.gemini/settings.json" 2>/dev/null || echo 'N/A')"

    # dcg hook should be removed
    ! grep -q '"command".*dcg' "$HOME/.gemini/settings.json"
}

# ============================================================================
# Aider Uninstall Tests
# ============================================================================

@test "uninstall: removes dcg settings from Aider config" {
    log_test "Testing Aider config removal..."

    cat > "$HOME/.aider.conf.yml" << 'EOF'
# Aider config
model: gpt-4

# Added by dcg installer - enables git hooks so dcg pre-commit can run
git-commit-verify: true
EOF

    "$UNINSTALL_SCRIPT" --yes --quiet

    log_test "After: $(cat "$HOME/.aider.conf.yml" 2>/dev/null || echo 'N/A')"

    # dcg-added lines should be removed
    ! grep -q "Added by dcg installer" "$HOME/.aider.conf.yml"
    # Other settings should remain
    grep -q "model: gpt-4" "$HOME/.aider.conf.yml"
}

@test "uninstall: removes empty Aider config file" {
    log_test "Testing Aider config removal when file becomes empty..."

    cat > "$HOME/.aider.conf.yml" << 'EOF'
# Added by dcg installer - enables git hooks so dcg pre-commit can run
git-commit-verify: true
EOF

    "$UNINSTALL_SCRIPT" --yes --quiet

    # File should be removed if it's now empty
    [ ! -f "$HOME/.aider.conf.yml" ]
}

# ============================================================================
# Binary Removal Tests
# ============================================================================

@test "uninstall: removes dcg binary" {
    log_test "Testing binary removal..."

    # Verify binary exists
    [ -f "$HOME/.local/bin/dcg" ]

    "$UNINSTALL_SCRIPT" --yes --quiet

    # Binary should be removed
    [ ! -f "$HOME/.local/bin/dcg" ]
}

# ============================================================================
# Configuration/Data Removal Tests
# ============================================================================

@test "uninstall: removes config directory by default" {
    log_test "Testing config directory removal..."

    mkdir -p "$HOME/.config/dcg"
    echo "test" > "$HOME/.config/dcg/config.toml"

    "$UNINSTALL_SCRIPT" --yes --quiet

    # Config directory should be removed
    [ ! -d "$HOME/.config/dcg" ]
}

@test "uninstall: keeps config directory with --keep-config" {
    log_test "Testing --keep-config flag..."

    mkdir -p "$HOME/.config/dcg"
    echo "test" > "$HOME/.config/dcg/config.toml"

    "$UNINSTALL_SCRIPT" --yes --quiet --keep-config

    # Config directory should still exist
    [ -d "$HOME/.config/dcg" ]
    [ -f "$HOME/.config/dcg/config.toml" ]
}

@test "uninstall: removes data directory by default" {
    log_test "Testing data directory removal..."

    mkdir -p "$HOME/.local/share/dcg"
    echo "test" > "$HOME/.local/share/dcg/history.db"

    "$UNINSTALL_SCRIPT" --yes --quiet

    # Data directory should be removed
    [ ! -d "$HOME/.local/share/dcg" ]
}

@test "uninstall: keeps data directory with --keep-history" {
    log_test "Testing --keep-history flag..."

    mkdir -p "$HOME/.local/share/dcg"
    echo "test" > "$HOME/.local/share/dcg/history.db"

    "$UNINSTALL_SCRIPT" --yes --quiet --keep-history

    # Data directory should still exist
    [ -d "$HOME/.local/share/dcg" ]
}

# ============================================================================
# Edge Cases
# ============================================================================

@test "uninstall: handles missing installations gracefully" {
    log_test "Testing graceful handling of missing installation..."

    # Remove everything
    rm -rf "$HOME/.claude" "$HOME/.gemini" "$HOME/.config/dcg" "$HOME/.local/share/dcg"
    rm -f "$HOME/.local/bin/dcg" "$HOME/.aider.conf.yml"

    # Should exit cleanly
    "$UNINSTALL_SCRIPT" --yes --quiet
}

@test "uninstall: syntax check passes" {
    log_test "Testing script syntax..."

    bash -n "$UNINSTALL_SCRIPT"
}

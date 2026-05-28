#!/bin/bash
# SessionStart hook template
#
# Runs when a Claude Code session begins.
# Use for initialization, environment checks, or notifications.
#
# Copy this template and customize for your plugin:
#   cp ${CLAUDE_PLUGIN_ROOT}/skills/create-hook/templates/sessionstart.sh \
#      your-plugin/hooks/init.sh
#
# Environment variables available:
#   CLAUDE_PROJECT_DIR - Current project directory
#   CLAUDE_PLUGIN_ROOT - This plugin's root directory
#   CLAUDE_ENV_FILE    - File to write persistent env vars

# =============================================================================
# ENVIRONMENT CHECKS
# =============================================================================

# Example: Check for required tools
# if ! command -v uv &> /dev/null; then
#     echo "Warning: uv not found. Some features may not work."
# fi

# =============================================================================
# PROJECT DETECTION
# =============================================================================

# Example: Detect project type and set variables
# if [ -f "${CLAUDE_PROJECT_DIR}/pyproject.toml" ]; then
#     echo "Detected Python project"
# fi

# =============================================================================
# NOTIFICATIONS
# =============================================================================

# Example: Show welcome message or warnings
# echo "Plugin initialized successfully"

# Exit successfully (don't block session start)
exit 0

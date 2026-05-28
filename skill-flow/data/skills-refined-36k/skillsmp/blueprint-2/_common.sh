#!/bin/bash
# Blueprint Common Functions
# Source this file in submodule scripts
#
# Usage: source "$(dirname "$0")/../_common.sh"

# Project root detection with fallback
# When sourced from submodule: ../../.. goes to project root
# Path: .claude/skills/blueprint/_common.sh → ../../.. → project root
get_project_root() {
  if [ -n "$CLAUDE_PROJECT_DIR" ]; then
    echo "$CLAUDE_PROJECT_DIR"
  else
    # From .claude/skills/blueprint/_common.sh, go up 3 levels to project root
    cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd
  fi
}

# Initialize PROJECT_ROOT for scripts that source this file
PROJECT_ROOT="$(get_project_root)"

# =============================================================================
# User-Level Path Resolution
# =============================================================================

# Convert absolute path to directory name
# Example: /Users/me/projects/blueprint → Users-me-projects-blueprint
# Example: /Users/me/Individual Project → Users-me-Individual-Project
path_to_dirname() {
  local path="$1"
  path="${path#/}"        # Remove leading /
  path="${path// /-}"     # Replace spaces with -
  echo "${path//\//-}"    # Replace / with -
}

# =============================================================================
# Project Path Resolution (Monorepo Support)
# =============================================================================

# Get project path with git root detection
# Priority: CLAUDE_PROJECT_DIR > git root > cwd
# This enables blueprint commands to work from subdirectories in monorepos
get_project_path() {
  if [ -n "$CLAUDE_PROJECT_DIR" ]; then
    echo "$CLAUDE_PROJECT_DIR"
  elif git rev-parse --show-toplevel &>/dev/null 2>&1; then
    git rev-parse --show-toplevel
  else
    pwd
  fi
}

# =============================================================================
# Alias Resolution (Cross-Machine Project Identity)
# =============================================================================

# Registry file location
BLUEPRINT_REGISTRY="$HOME/.claude/blueprint/projects/.projects"

# Check if jq is available (cached per session)
_check_jq() {
  if [ -n "${_JQ_AVAILABLE+x}" ]; then
    return "$_JQ_AVAILABLE"
  fi

  if command -v jq &> /dev/null; then
    _JQ_AVAILABLE=0
  else
    _JQ_AVAILABLE=1
    if [ -z "${_JQ_WARNING_SHOWN:-}" ]; then
      echo "[WARNING] jq not found. Project alias resolution disabled." >&2
      export _JQ_WARNING_SHOWN=1
    fi
  fi
  return "$_JQ_AVAILABLE"
}

# Resolve project alias from registry
# Returns: alias string if found, empty string otherwise
resolve_project_alias() {
  local current_path="${1:-$(get_project_path)}"

  # Registry must exist
  [ -f "$BLUEPRINT_REGISTRY" ] || return 0

  # jq must be available
  _check_jq || return 0

  # Search for matching path in registry
  local alias_name
  alias_name=$(jq -r --arg path "$current_path" \
    '.projects[] | select(.paths[] == $path) | .alias' \
    "$BLUEPRINT_REGISTRY" 2>/dev/null | head -n1)

  echo "$alias_name"
}

# Initialize registry file if not exists
init_registry() {
  local registry_dir="$HOME/.claude/blueprint/projects"

  [ -d "$registry_dir" ] || mkdir -p "$registry_dir"

  if [ ! -f "$BLUEPRINT_REGISTRY" ]; then
    echo '{"version":"1.0.0","projects":[]}' > "$BLUEPRINT_REGISTRY"
  fi
}

# Get blueprint data directory for current project
# Priority: alias-based → path-based (fallback)
# Returns: ~/.claude/blueprint/projects/{alias}/ or ~/.claude/blueprint/projects/{path-based}/
get_blueprint_data_dir() {
  local project_path
  project_path=$(get_project_path)

  # Try alias resolution first
  local alias_name
  alias_name=$(resolve_project_alias "$project_path")

  if [ -n "$alias_name" ]; then
    echo "$HOME/.claude/blueprint/projects/$alias_name"
  else
    # Fallback to path-based directory
    local dirname
    dirname=$(path_to_dirname "$project_path")
    echo "$HOME/.claude/blueprint/projects/$dirname"
  fi
}

# Check if project is initialized for Blueprint
# Exits with error if not initialized
check_project_initialized() {
  local data_dir
  data_dir=$(get_blueprint_data_dir)

  if [ ! -d "$data_dir" ]; then
    error "Blueprint not initialized for this project."
    echo "" >&2
    echo "Project: $(get_project_path)" >&2
    echo "Expected: $data_dir" >&2
    echo "" >&2
    echo "Run 'blueprint project init <alias>' to initialize Blueprint for this project." >&2
    exit 1
  fi
}

# Initialize BLUEPRINT_DATA_DIR for scripts that source this file
# Note: Does NOT check initialization - scripts should call check_project_initialized() if needed
BLUEPRINT_DATA_DIR="$(get_blueprint_data_dir)"

# =============================================================================
# FrontMatter Utilities
# =============================================================================

# Extract FrontMatter from file (between first and second ---)
# Supports both .md and .yaml files
get_frontmatter() {
  local file="$1"
  if [[ "$file" == *.yaml ]]; then
    # YAML: entire file is structured data
    cat "$file" 2>/dev/null
  else
    # Markdown: extract --- block
    awk '/^---$/{if(++c==2)exit}c' "$file" 2>/dev/null
  fi
}

# Extract field value from FrontMatter
get_field() {
  local frontmatter="$1"
  local field="$2"
  echo "$frontmatter" | grep "^${field}:" | sed "s/^${field}:[[:space:]]*//" | sed 's/^"//' | sed 's/"$//'
}

# Extract description from FrontMatter
get_description() {
  local file="$1"
  local frontmatter
  frontmatter=$(get_frontmatter "$file")
  local desc
  desc=$(get_field "$frontmatter" "description")
  if [ -z "$desc" ]; then
    echo "(no description)"
  else
    echo "$desc"
  fi
}

# Print error message to stderr
error() {
  echo "[ERROR] $*" >&2
}

# Print info message
info() {
  echo "[INFO] $*"
}

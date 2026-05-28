#!/bin/bash
# Blueprint Project Submodule
# Manage project aliases for cross-machine portability
#
# Usage: blueprint project <command> [args]

set -e

source "$(dirname "$0")/../_common.sh"

COMMAND="$1"

# =============================================================================
# Help
# =============================================================================

show_help() {
  cat << 'EOF'
Project - Manage project aliases for cross-machine portability

Usage:
  blueprint project init <alias> [--notes "text"]   Initialize new project
  blueprint project list                            List all projects
  blueprint project show <alias>                    Show project details
  blueprint project remove <alias>                  Remove project
  blueprint project link <alias>                    Link current path to project
  blueprint project unlink <alias> [path]           Unlink path from project
  blueprint project rename <new-alias>              Rename project alias
  blueprint project manage                          Scan and manage projects
  blueprint project current [--data]                Show current project info

Options:
  -h, --help    Show this help message

Examples:
  blueprint project init myproject
  blueprint project init myproject --notes "My awesome project"
  blueprint project list
  blueprint project show myproject
  blueprint project link myproject
  blueprint project unlink myproject /old/path
  blueprint project rename my-new-alias
  blueprint project manage
  blueprint project current
  blueprint project current --data
EOF
}

# =============================================================================
# Utility Functions
# =============================================================================

require_jq() {
  if ! command -v jq &> /dev/null; then
    error "jq is required for project management."
    echo "Install jq: https://stedolan.github.io/jq/download/"
    exit 1
  fi
}

# =============================================================================
# Commands
# =============================================================================

do_init() {
  local alias_name="$1"
  shift || true
  local notes=""

  # Parse --notes flag
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --notes)
        notes="$2"
        shift 2
        ;;
      *)
        error "Unknown option: $1"
        exit 1
        ;;
    esac
  done

  if [ -z "$alias_name" ]; then
    echo "Usage: blueprint project init <alias> [--notes \"text\"]"
    exit 1
  fi

  require_jq

  local current_path
  current_path="${CLAUDE_PROJECT_DIR:-$(pwd)}"

  # Validate alias format
  if ! [[ "$alias_name" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    error "Invalid alias. Use alphanumeric characters, dashes, and underscores only."
    exit 1
  fi

  # Initialize registry if needed
  init_registry

  # Check if path already registered
  local existing_alias
  existing_alias=$(resolve_project_alias "$current_path")
  if [ -n "$existing_alias" ]; then
    error "Path already registered as '$existing_alias'."
    echo "Use 'blueprint project show $existing_alias' to view details."
    exit 1
  fi

  # Check if alias exists
  if jq -e --arg a "$alias_name" '.projects[] | select(.alias == $a)' "$BLUEPRINT_REGISTRY" >/dev/null 2>&1; then
    error "Alias '$alias_name' already exists."
    echo "Use 'blueprint project link $alias_name' to add current path."
    exit 1
  fi

  local data_dir="$HOME/.claude/blueprint/projects/$alias_name"

  # Check for legacy directory
  local legacy_dirname
  legacy_dirname=$(path_to_dirname "$current_path")
  local legacy_dir="$HOME/.claude/blueprint/projects/$legacy_dirname"

  if [ -d "$legacy_dir" ] && [ ! -d "$data_dir" ]; then
    info "Found existing data at $legacy_dir"
    info "Renaming to $data_dir"
    mv "$legacy_dir" "$data_dir"
  elif [ ! -d "$data_dir" ]; then
    # Create new data directory with all required subdirectories
    mkdir -p "$data_dir/constitutions"
    mkdir -p "$data_dir/forms"
    mkdir -p "$data_dir/front-matters"
    mkdir -p "$data_dir/gates"
    mkdir -p "$data_dir/templates"
    mkdir -p "$data_dir/plans"

    # Try to copy framework files from various sources
    local source_dir=""
    local base_dir="$HOME/.claude/blueprint/base"

    # Check user-level base files first (from install-global.sh)
    if [ -d "$base_dir/constitutions" ]; then
      source_dir="$base_dir"
    # Check environment variable
    elif [ -n "${BLUEPRINT_FRAMEWORK_DIR:-}" ] && [ -d "$BLUEPRINT_FRAMEWORK_DIR/core" ]; then
      source_dir="$BLUEPRINT_FRAMEWORK_DIR/core"
    # Check project root (for development)
    elif [ -d "$PROJECT_ROOT/core" ]; then
      source_dir="$PROJECT_ROOT/core"
    fi

    if [ -n "$source_dir" ]; then
      [ -d "$source_dir/constitutions" ] && rsync -a "$source_dir/constitutions/" "$data_dir/constitutions/"
      [ -d "$source_dir/forms" ] && rsync -a "$source_dir/forms/" "$data_dir/forms/"
      [ -d "$source_dir/front-matters" ] && rsync -a "$source_dir/front-matters/" "$data_dir/front-matters/"
      [ -d "$source_dir/gates" ] && rsync -a "$source_dir/gates/" "$data_dir/gates/"
      [ -d "$source_dir/templates" ] && rsync -a "$source_dir/templates/" "$data_dir/templates/"
    fi
  fi

  # Add to registry
  local tmp_file
  tmp_file=$(mktemp)
  jq --arg alias "$alias_name" \
     --arg path "$current_path" \
     --arg notes "$notes" \
     '.projects += [{"alias": $alias, "paths": [$path], "notes": $notes}]' \
     "$BLUEPRINT_REGISTRY" > "$tmp_file" && mv "$tmp_file" "$BLUEPRINT_REGISTRY"

  echo ""
  info "Project initialized: $alias_name"
  echo "  Path: $current_path"
  echo "  Data: $data_dir"
  [ -n "$notes" ] && echo "  Notes: $notes"
}

do_list() {
  require_jq
  init_registry

  local count
  count=$(jq '.projects | length' "$BLUEPRINT_REGISTRY")

  if [ "$count" -eq 0 ]; then
    echo "No projects registered."
    echo ""
    echo "Run 'blueprint project init <alias>' to register a project."
    exit 0
  fi

  echo "Projects ($count):"
  echo ""

  jq -r '.projects[] | "\(.alias)\t\(.paths | length)\t\(.notes // "-")"' "$BLUEPRINT_REGISTRY" | \
    while IFS=$'\t' read -r alias_name paths notes; do
      printf "  %-16s (%d paths)  %s\n" "$alias_name" "$paths" "$notes"
    done
}

do_show() {
  local alias_name="$1"

  if [ -z "$alias_name" ]; then
    echo "Usage: blueprint project show <alias>"
    exit 1
  fi

  require_jq
  init_registry

  local project
  project=$(jq -e --arg a "$alias_name" '.projects[] | select(.alias == $a)' "$BLUEPRINT_REGISTRY" 2>/dev/null)

  if [ -z "$project" ]; then
    error "Project '$alias_name' not found."
    echo ""
    echo "Available projects:"
    do_list
    exit 1
  fi

  echo "Project: $alias_name"
  echo "Notes: $(echo "$project" | jq -r '.notes // "-"')"
  echo "Paths:"
  echo "$project" | jq -r '.paths[]' | while read -r path; do
    echo "  - $path"
  done
  echo "Data: ~/.claude/blueprint/projects/$alias_name/"
}

do_remove() {
  local alias_name=""
  local remove_registry=false
  local remove_data_dir=false

  # Parse arguments
  while [ $# -gt 0 ]; do
    case "$1" in
      --registry)
        remove_registry=true
        shift
        ;;
      --data-dir)
        remove_data_dir=true
        shift
        ;;
      -*)
        error "Unknown option: $1"
        exit 1
        ;;
      *)
        alias_name="$1"
        shift
        ;;
    esac
  done

  if [ -z "$alias_name" ]; then
    echo "Usage: blueprint project remove <alias> --registry [--data-dir]"
    exit 1
  fi

  require_jq
  init_registry

  # Check exists
  if ! jq -e --arg a "$alias_name" '.projects[] | select(.alias == $a)' "$BLUEPRINT_REGISTRY" >/dev/null 2>&1; then
    error "Project '$alias_name' not found."
    exit 1
  fi

  if [ "$remove_registry" = false ]; then
    error "Specify what to remove:"
    echo "  blueprint project remove $alias_name --registry             # Registry only"
    echo "  blueprint project remove $alias_name --registry --data-dir  # Registry + data"
    exit 1
  fi

  # Delete data directory if requested
  local data_dir="$HOME/.claude/blueprint/projects/$alias_name"
  if [ "$remove_data_dir" = true ] && [ -d "$data_dir" ]; then
    rm -rf "$data_dir"
    info "Data directory deleted."
  fi

  # Remove from registry
  local tmp_file
  tmp_file=$(mktemp)
  jq --arg a "$alias_name" 'del(.projects[] | select(.alias == $a))' "$BLUEPRINT_REGISTRY" > "$tmp_file" && mv "$tmp_file" "$BLUEPRINT_REGISTRY"

  info "Project '$alias_name' removed from registry."
}

do_link() {
  local alias_name="$1"
  local current_path
  current_path="${CLAUDE_PROJECT_DIR:-$(pwd)}"

  if [ -z "$alias_name" ]; then
    echo "Usage: blueprint project link <alias>"
    exit 1
  fi

  require_jq
  init_registry

  # Check alias exists
  if ! jq -e --arg a "$alias_name" '.projects[] | select(.alias == $a)' "$BLUEPRINT_REGISTRY" >/dev/null 2>&1; then
    error "Project '$alias_name' not found."
    echo ""
    echo "Available projects:"
    do_list
    exit 1
  fi

  # Check path not already linked
  local existing
  existing=$(jq -r --arg a "$alias_name" --arg p "$current_path" \
    '.projects[] | select(.alias == $a) | .paths[] | select(. == $p)' "$BLUEPRINT_REGISTRY")

  if [ -n "$existing" ]; then
    error "Path already linked to '$alias_name'."
    exit 1
  fi

  # Add path
  local tmp_file
  tmp_file=$(mktemp)
  jq --arg a "$alias_name" --arg p "$current_path" \
    '(.projects[] | select(.alias == $a) | .paths) += [$p]' \
    "$BLUEPRINT_REGISTRY" > "$tmp_file" && mv "$tmp_file" "$BLUEPRINT_REGISTRY"

  info "Path linked to '$alias_name'."
  echo "  $current_path"
}

do_unlink() {
  local alias_name="$1"
  local path="${2:-${CLAUDE_PROJECT_DIR:-$(pwd)}}"

  if [ -z "$alias_name" ]; then
    echo "Usage: blueprint project unlink <alias> [path]"
    exit 1
  fi

  require_jq
  init_registry

  # Check alias exists
  local project
  project=$(jq -e --arg a "$alias_name" '.projects[] | select(.alias == $a)' "$BLUEPRINT_REGISTRY" 2>/dev/null)

  if [ -z "$project" ]; then
    error "Project '$alias_name' not found."
    exit 1
  fi

  # Check path count
  local path_count
  path_count=$(echo "$project" | jq '.paths | length')

  if [ "$path_count" -eq 1 ]; then
    echo "Warning: This is the last path for '$alias_name'."
    read -p "Remove project entirely? [y/N] " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
      do_remove "$alias_name" --registry
      return
    else
      echo "Cancelled."
      exit 0
    fi
  fi

  # Remove path
  local tmp_file
  tmp_file=$(mktemp)
  jq --arg a "$alias_name" --arg p "$path" \
    '(.projects[] | select(.alias == $a) | .paths) -= [$p]' \
    "$BLUEPRINT_REGISTRY" > "$tmp_file" && mv "$tmp_file" "$BLUEPRINT_REGISTRY"

  info "Path unlinked from '$alias_name'."
}

do_rename() {
  local new_alias="$1"
  local current_path="${CLAUDE_PROJECT_DIR:-$(pwd)}"

  if [ -z "$new_alias" ]; then
    echo "Usage: blueprint project rename <new-alias>"
    exit 1
  fi

  require_jq

  # Validate new alias format
  if ! [[ "$new_alias" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    error "Invalid alias. Use alphanumeric characters, dashes, and underscores only."
    exit 1
  fi

  init_registry

  # Check new alias not already taken
  if jq -e --arg a "$new_alias" '.projects[] | select(.alias == $a)' "$BLUEPRINT_REGISTRY" >/dev/null 2>&1; then
    error "Alias '$new_alias' already exists."
    exit 1
  fi

  # Find current project by path
  local current_alias
  current_alias=$(resolve_project_alias "$current_path")

  local old_dir=""
  local is_registered=false

  if [ -n "$current_alias" ]; then
    # Project is registered
    is_registered=true
    old_dir="$HOME/.claude/blueprint/projects/$current_alias"
  else
    # Project not registered - check for legacy path-based directory
    local legacy_dirname
    legacy_dirname=$(path_to_dirname "$current_path")
    local legacy_dir="$HOME/.claude/blueprint/projects/$legacy_dirname"

    if [ -d "$legacy_dir" ]; then
      old_dir="$legacy_dir"
      current_alias="$legacy_dirname"
    else
      error "No project data found for current path."
      echo "Use 'blueprint project init $new_alias' to create a new project."
      exit 1
    fi
  fi

  local new_dir="$HOME/.claude/blueprint/projects/$new_alias"

  # Rename data directory
  if [ "$old_dir" != "$new_dir" ]; then
    if [ -d "$new_dir" ]; then
      error "Directory already exists: $new_dir"
      exit 1
    fi
    mv "$old_dir" "$new_dir"
    info "Renamed: $old_dir → $new_dir"
  fi

  # Update or create registry entry
  local tmp_file
  tmp_file=$(mktemp)

  if [ "$is_registered" = true ]; then
    # Update existing entry
    jq --arg old "$current_alias" --arg new "$new_alias" \
      '(.projects[] | select(.alias == $old) | .alias) = $new' \
      "$BLUEPRINT_REGISTRY" > "$tmp_file" && mv "$tmp_file" "$BLUEPRINT_REGISTRY"
  else
    # Create new entry for unregistered project
    jq --arg alias "$new_alias" --arg path "$current_path" \
      '.projects += [{"alias": $alias, "paths": [$path], "notes": ""}]' \
      "$BLUEPRINT_REGISTRY" > "$tmp_file" && mv "$tmp_file" "$BLUEPRINT_REGISTRY"
  fi

  echo ""
  info "Project renamed: $current_alias → $new_alias"
  echo "  Path: $current_path"
  echo "  Data: $new_dir"
}

do_current() {
  local show_data=false

  # Parse flags
  while [ $# -gt 0 ]; do
    case "$1" in
      --data)
        show_data=true
        shift
        ;;
      -*)
        error "Unknown option: $1"
        exit 1
        ;;
      *)
        shift
        ;;
    esac
  done

  local current_path
  current_path=$(get_project_path)
  local data_dir
  data_dir=$(get_blueprint_data_dir "$current_path")

  # Check if project exists
  if [ ! -d "$data_dir" ]; then
    error "No project data found for current path."
    echo "Run 'blueprint project init <alias>' to initialize."
    exit 1
  fi

  local alias_name
  alias_name=$(resolve_project_alias "$current_path")
  if [ -z "$alias_name" ]; then
    alias_name=$(basename "$data_dir")
  fi

  # Output based on flags
  if [ "$show_data" = true ]; then
    echo "$data_dir"
  else
    echo "Alias: $alias_name"
    echo "Data: $data_dir"
  fi
}

do_manage() {
  require_jq
  init_registry

  local blueprint_dir="$HOME/.claude/blueprint/projects"
  local unregistered_count=0
  local pathbased_count=0
  local unregistered_valid=()
  local unregistered_invalid=()
  local pathbased_projects=()

  echo "Scanning projects..."
  echo ""

  # Required directories for valid structure
  local required_dirs=("constitutions" "forms" "front-matters" "gates" "templates" "plans")

  # Step 1: Scan for unregistered projects
  for dir in "$blueprint_dir"/*/; do
    [ -d "$dir" ] || continue

    local dirname
    dirname=$(basename "$dir")

    # Skip registry file and hidden dirs
    [[ "$dirname" == "."* ]] && continue

    # Check if registered
    local is_registered
    is_registered=$(jq -r --arg a "$dirname" '.projects[] | select(.alias == $a) | .alias' "$BLUEPRINT_REGISTRY" 2>/dev/null)

    if [ -z "$is_registered" ]; then
      # Unregistered - validate structure
      local missing_dirs=()
      for req_dir in "${required_dirs[@]}"; do
        [ ! -d "$dir$req_dir" ] && missing_dirs+=("$req_dir/")
      done

      if [ ${#missing_dirs[@]} -eq 0 ]; then
        unregistered_valid+=("$dirname")
      else
        unregistered_invalid+=("$dirname:${missing_dirs[*]}")
      fi
      ((unregistered_count++))
    else
      # Registered - check if path-based alias
      # Path-based aliases contain multiple dashes and typically start with capital letter
      if [[ "$dirname" =~ ^[A-Z][a-zA-Z0-9]*-[a-zA-Z0-9]+-.*$ ]]; then
        pathbased_projects+=("$dirname")
        ((pathbased_count++))
      fi
    fi
  done

  # Output unregistered projects
  if [ ${#unregistered_valid[@]} -gt 0 ] || [ ${#unregistered_invalid[@]} -gt 0 ]; then
    echo "Unregistered Projects ($unregistered_count):"
    echo ""

    for proj in "${unregistered_valid[@]}"; do
      # Suggest alias from directory name
      local suggested
      suggested=$(echo "$proj" | sed 's/.*-//' | tr '[:upper:]' '[:lower:]')
      echo "  $proj/"
      echo "    Status: Valid structure"
      echo "    Suggested alias: $suggested"
      echo "    Action: Run 'blueprint project rename $suggested'"
      echo ""
    done

    for entry in "${unregistered_invalid[@]}"; do
      local proj="${entry%%:*}"
      local missing="${entry#*:}"
      echo "  $proj/"
      echo "    Status: Invalid (missing: $missing)"
      echo "    Action: Consider cleanup or manual repair"
      echo ""
    done
  fi

  # Output path-based registered projects
  if [ ${#pathbased_projects[@]} -gt 0 ]; then
    echo "path-based Registered Projects ($pathbased_count):"
    echo ""

    for proj in "${pathbased_projects[@]}"; do
      local suggested
      suggested=$(echo "$proj" | sed 's/.*-//' | tr '[:upper:]' '[:lower:]')
      echo "  $proj/"
      echo "    Current alias: $proj"
      echo "    Suggested alias: $suggested"
      echo "    Action: Run 'blueprint project rename $suggested'"
      echo ""
    done
  fi

  # Summary
  echo "Summary: $unregistered_count unregistered, $pathbased_count path-based"

  if [ $unregistered_count -eq 0 ] && [ $pathbased_count -eq 0 ]; then
    echo ""
    info "All projects are properly registered with custom aliases."
  fi
}

# =============================================================================
# Main Dispatch
# =============================================================================

case "$COMMAND" in
  init)
    shift
    do_init "$@"
    ;;
  list)
    do_list
    ;;
  show)
    shift
    do_show "$@"
    ;;
  remove)
    shift
    do_remove "$@"
    ;;
  link)
    shift
    do_link "$@"
    ;;
  unlink)
    shift
    do_unlink "$@"
    ;;
  rename)
    shift
    do_rename "$@"
    ;;
  manage)
    do_manage
    ;;
  current)
    shift
    do_current "$@"
    ;;
  -h|--help|"")
    show_help
    ;;
  *)
    error "Unknown command: $COMMAND"
    echo ""
    show_help
    exit 1
    ;;
esac

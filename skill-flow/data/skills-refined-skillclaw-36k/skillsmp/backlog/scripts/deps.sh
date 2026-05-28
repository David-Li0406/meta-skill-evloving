#!/bin/bash
#
# deps.sh - Dependency resolution utilities for task management
# Compatible with bash 3.2+ (macOS default)
#
# Provides:
# - Dependency graph building from INDEX.md
# - Cycle detection
# - Status computation (auto-block/unblock based on dependencies)
# - Cross-repo dependency support
# - Critical path analysis
# - ASCII visualization
#
# Usage:
#   source deps.sh
#   deps_build_graph           # Build dependency graph from INDEX.md
#   deps_check_cycles          # Detect circular dependencies
#   deps_get_status <id>       # Get stored status for a task
#   deps_get_deps <id>         # Get dependencies for a task
#   deps_get_blockers <id>     # Get list of incomplete dependencies
#   deps_get_dependents <id>   # Get list of tasks that depend on this one
#   deps_can_launch <id>       # Check if task can be launched (deps complete)
#   deps_visualize             # ASCII dependency graph
#

set -euo pipefail

# Configuration
DEPS_VERBOSE="${DEPS_VERBOSE:-false}"
DEPS_CROSS_REPO="${DEPS_CROSS_REPO:-true}"

# Temp directory for graph data (cleaned up on exit)
DEPS_TMP_DIR=""

# Initialize temp directory
deps_init_tmp() {
  if [[ -z "$DEPS_TMP_DIR" || ! -d "$DEPS_TMP_DIR" ]]; then
    DEPS_TMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/deps.XXXXXX")
    mkdir -p "$DEPS_TMP_DIR/status"
    mkdir -p "$DEPS_TMP_DIR/deps"
    mkdir -p "$DEPS_TMP_DIR/rdeps"
    mkdir -p "$DEPS_TMP_DIR/title"
    mkdir -p "$DEPS_TMP_DIR/repo"
    : > "$DEPS_TMP_DIR/all_tasks"
  fi
}

# Cleanup temp directory
deps_cleanup() {
  if [[ -n "$DEPS_TMP_DIR" && -d "$DEPS_TMP_DIR" ]]; then
    rm -rf "$DEPS_TMP_DIR"
  fi
}

# Log function
deps_log() {
  if [[ "$DEPS_VERBOSE" == "true" ]]; then
    echo "[deps] $*" >&2
  fi
}

# Store a value for a task
deps_set() {
  local category="$1"  # status, deps, rdeps, title, repo
  local task_id="$2"
  local value="$3"
  deps_init_tmp
  # Sanitize task_id for filename (replace / with _)
  local safe_id="${task_id//\//_}"
  echo "$value" > "$DEPS_TMP_DIR/$category/$safe_id"
}

# Get a value for a task
deps_get() {
  local category="$1"
  local task_id="$2"
  deps_init_tmp
  local safe_id="${task_id//\//_}"
  local file="$DEPS_TMP_DIR/$category/$safe_id"
  if [[ -f "$file" ]]; then
    cat "$file"
  fi
}

# Append a value (for lists like rdeps)
deps_append() {
  local category="$1"
  local task_id="$2"
  local value="$3"
  deps_init_tmp
  local safe_id="${task_id//\//_}"
  local file="$DEPS_TMP_DIR/$category/$safe_id"
  local current=""
  if [[ -f "$file" ]]; then
    current=$(cat "$file")
  fi
  if [[ -n "$current" ]]; then
    echo "$current $value" > "$file"
  else
    echo "$value" > "$file"
  fi
}

# Get all task IDs
deps_all_tasks() {
  deps_init_tmp
  if [[ -f "$DEPS_TMP_DIR/all_tasks" ]]; then
    cat "$DEPS_TMP_DIR/all_tasks"
  fi
}

# Add a task ID to the list
deps_add_task() {
  local task_id="$1"
  deps_init_tmp
  echo "$task_id" >> "$DEPS_TMP_DIR/all_tasks"
}

# Parse a single INDEX.md file and add to graph
# Args: <path-to-index-md> <repo-prefix>
deps_parse_index() {
  local index_file="$1"
  local repo_prefix="${2:-}"

  if [[ ! -f "$index_file" ]]; then
    deps_log "Index file not found: $index_file"
    return 1
  fi

  deps_log "Parsing $index_file"

  # Track whether we've found the task table header
  local in_task_table=false

  # Parse the table rows from INDEX.md
  # Format: | ID | Title | Status | Dependencies | Worktree |
  while IFS= read -r line; do
    # Skip empty lines
    [[ -z "$line" ]] && continue

    # Skip non-table lines
    [[ ! "$line" =~ ^\|.*\|$ ]] && continue

    # Detect task table header row: must have ID, Title, Status columns
    if [[ "$line" =~ ^[[:space:]]*\|[[:space:]]*ID[[:space:]]*\|.*Title.*\|.*Status.*\| ]]; then
      in_task_table=true
      deps_log "  Found task table header"
      continue
    fi

    # Skip separator rows (|---|---|...)
    [[ "$line" =~ ^[[:space:]]*\|[[:space:]]*[-:]+[[:space:]]*\| ]] && continue

    # If we hit another header row (different table), stop parsing task table
    if [[ "$line" =~ ^[[:space:]]*\|[[:space:]]*[A-Za-z]+[[:space:]]*\|.*\|.*\| ]] && \
       [[ ! "$line" =~ ^[[:space:]]*\|[[:space:]]*[A-Z]+-[0-9]+ ]]; then
      # This looks like a header row for a different table
      if [[ "$in_task_table" == "true" ]]; then
        deps_log "  Found different table header, stopping task parsing"
        in_task_table=false
      fi
      continue
    fi

    # Only parse rows if we're in the task table
    [[ "$in_task_table" != "true" ]] && continue

    # Parse table row - remove leading/trailing pipes
    line="${line#|}"
    line="${line%|}"

    # Split by | using read
    local id="" title="" status="" deps="" worktree=""
    local i=0
    local OLD_IFS="$IFS"
    IFS='|'
    for col in $line; do
      # Trim whitespace
      col=$(echo "$col" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
      case $i in
        0) id="$col" ;;
        1) title="$col" ;;
        2) status="$col" ;;
        3) deps="$col" ;;
        4) worktree="$col" ;;
      esac
      i=$((i + 1))
    done
    IFS="$OLD_IFS"

    # STRICT: Only accept IDs matching the task ID pattern (PREFIX-NNN)
    # This prevents parsing documentation tables as tasks
    if [[ ! "$id" =~ ^[A-Z]+-[0-9]+$ ]]; then
      deps_log "  Skipping non-task row: $id"
      continue
    fi

    deps_log "  Found task: $id ($status) deps=[$deps]"

    # Store task info
    deps_add_task "$id"
    deps_set status "$id" "$status"
    deps_set title "$id" "$title"

    # Extract repo prefix from ID (e.g., CRANE-001 -> CRANE)
    if [[ "$id" =~ ^([A-Z]+)-[0-9]+ ]]; then
      deps_set repo "$id" "${BASH_REMATCH[1]}"
    else
      deps_set repo "$id" "$repo_prefix"
    fi

    # Parse dependencies (comma or space separated, handle "None" and "-")
    local dep_list=""
    if [[ -n "$deps" && "$deps" != "-" && "$deps" != "None" && "$deps" != "none" ]]; then
      # Split by comma or space, extract task IDs
      for dep in $(echo "$deps" | tr ',' ' '); do
        dep=$(echo "$dep" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        # Extract just the task ID if there's extra text
        if [[ "$dep" =~ ([A-Z]+-[0-9]+) ]]; then
          local dep_id="${BASH_REMATCH[1]}"
          if [[ -n "$dep_list" ]]; then
            dep_list="$dep_list $dep_id"
          else
            dep_list="$dep_id"
          fi
          # Build reverse graph (who depends on this dep)
          deps_append rdeps "$dep_id" "$id"
        fi
      done
    fi

    deps_set deps "$id" "$dep_list"

  done < "$index_file"
}

# Build the complete dependency graph
deps_build_graph() {
  local repo_root
  repo_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

  # Reset temp directory
  deps_cleanup
  deps_init_tmp

  # Parse main repo INDEX.md
  if [[ -f "$repo_root/tasks/INDEX.md" ]]; then
    local prefix=""
    if [[ -f "$repo_root/design.yaml" ]]; then
      prefix=$(grep "^repo_prefix:" "$repo_root/design.yaml" 2>/dev/null | cut -d: -f2 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    fi
    deps_parse_index "$repo_root/tasks/INDEX.md" "$prefix"
  fi

  # Parse submodule INDEX.md files if cross-repo enabled
  if [[ "$DEPS_CROSS_REPO" == "true" ]]; then
    # Find all design.yaml files in submodules
    while IFS= read -r design_file; do
      [[ -z "$design_file" ]] && continue
      local submodule_dir
      submodule_dir=$(dirname "$design_file")
      local index_file="$submodule_dir/tasks/INDEX.md"

      if [[ -f "$index_file" ]]; then
        local prefix
        prefix=$(grep "^repo_prefix:" "$design_file" 2>/dev/null | cut -d: -f2 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        deps_parse_index "$index_file" "$prefix"
      fi
    done < <(find "$repo_root" -name "design.yaml" -type f 2>/dev/null | grep -v "^$repo_root/design.yaml$" | head -20)
  fi

  local count=$(deps_all_tasks | wc -l | tr -d ' ')
  deps_log "Graph built: $count tasks"
}

# Check if a task exists
deps_exists() {
  local task_id="$1"
  local status=$(deps_get status "$task_id")
  [[ -n "$status" ]]
}

# Get status for a task
deps_get_status() {
  local task_id="$1"
  deps_get status "$task_id"
}

# Get dependencies for a task
deps_get_deps() {
  local task_id="$1"
  deps_get deps "$task_id"
}

# Get title for a task
deps_get_title() {
  local task_id="$1"
  deps_get title "$task_id"
}

# Validate that a dependency ID exists
deps_validate() {
  local dep_id="$1"
  if deps_exists "$dep_id"; then
    return 0
  fi
  echo "Dependency not found: $dep_id" >&2
  return 1
}

# Get list of incomplete dependencies for a task
deps_get_blockers() {
  local task_id="$1"
  local deps=$(deps_get_deps "$task_id")
  local blockers=""

  for dep in $deps; do
    local dep_status=$(deps_get_status "$dep")
    # Not complete = blocking
    if [[ "$dep_status" != "Complete" ]]; then
      if [[ -n "$blockers" ]]; then
        blockers="$blockers $dep"
      else
        blockers="$dep"
      fi
    fi
  done

  echo "$blockers"
}

# Get list of tasks that depend on this one
deps_get_dependents() {
  local task_id="$1"
  deps_get rdeps "$task_id"
}

# Compute the effective status of a task based on dependencies
deps_compute_status() {
  local task_id="$1"
  local stored_status=$(deps_get_status "$task_id")

  # If already in progress, in review, or complete, keep that status
  case "$stored_status" in
    "In Progress"|"In Review"|"Review"|"Complete"|"Changes Requested")
      echo "$stored_status"
      return
      ;;
  esac

  # Check if blocked by dependencies
  local blockers=$(deps_get_blockers "$task_id")

  if [[ -n "$blockers" ]]; then
    echo "Blocked"
  else
    # All dependencies complete (or no dependencies)
    if [[ "$stored_status" == "Blocked" ]]; then
      echo "Ready"
    else
      echo "$stored_status"
    fi
  fi
}

# Check if a task can be launched (all dependencies complete)
deps_can_launch() {
  local task_id="$1"

  # Check task exists
  if ! deps_exists "$task_id"; then
    echo "Task not found: $task_id"
    return 1
  fi

  # Get blockers
  local blockers=$(deps_get_blockers "$task_id")

  if [[ -n "$blockers" ]]; then
    echo "Blocked by incomplete dependencies:"
    for blocker in $blockers; do
      local blocker_status=$(deps_get_status "$blocker")
      local blocker_title=$(deps_get_title "$blocker")
      echo "  - $blocker ($blocker_status): $blocker_title"
    done
    return 1
  fi

  return 0
}

# Check for circular dependencies using DFS with proper backtracking
deps_check_cycles() {
  deps_init_tmp
  local visited_file="$DEPS_TMP_DIR/cycle_visited"
  local on_path_file="$DEPS_TMP_DIR/cycle_on_path"

  : > "$visited_file"
  : > "$on_path_file"

  local found_cycle=""
  local cycle_path=""

  # Recursive DFS with proper backtracking
  # Uses files to track state since bash functions can't modify parent variables
  dfs_visit() {
    local node="$1"
    local path="$2"

    # Check if already fully visited (no cycle from this node)
    if grep -q "^${node}$" "$visited_file" 2>/dev/null; then
      return 0
    fi

    # Check if on current path (cycle detected!)
    if grep -q "^${node}$" "$on_path_file" 2>/dev/null; then
      found_cycle="$node"
      cycle_path="$path -> $node"
      return 1
    fi

    # Add to current path
    echo "$node" >> "$on_path_file"

    # Visit all dependencies
    local deps=$(deps_get_deps "$node")
    for dep in $deps; do
      if ! dfs_visit "$dep" "$path $node"; then
        return 1
      fi
    done

    # Remove from current path (backtrack)
    grep -v "^${node}$" "$on_path_file" > "$on_path_file.tmp" 2>/dev/null || true
    mv "$on_path_file.tmp" "$on_path_file" 2>/dev/null || : > "$on_path_file"

    # Mark as fully visited
    echo "$node" >> "$visited_file"

    return 0
  }

  # Check all nodes
  while IFS= read -r task; do
    [[ -z "$task" ]] && continue
    if ! grep -q "^${task}$" "$visited_file" 2>/dev/null; then
      if ! dfs_visit "$task" ""; then
        echo "Circular dependency detected!"
        echo "Cycle: $cycle_path"
        return 1
      fi
    fi
  done < <(deps_all_tasks)

  deps_log "No cycles detected"
  return 0
}

# Generate ASCII visualization of dependency graph
deps_visualize() {
  echo ""
  echo "Dependency Graph"
  echo "================"
  echo ""

  while IFS= read -r task; do
    [[ -z "$task" ]] && continue

    local status=$(deps_get_status "$task")
    local deps=$(deps_get_deps "$task")
    local dependents=$(deps_get_dependents "$task")

    # Status indicator
    local indicator
    case "$status" in
      "Complete") indicator="[x]" ;;
      "In Progress") indicator="[>]" ;;
      "In Review"|"Review") indicator="[?]" ;;
      "Ready") indicator="[ ]" ;;
      "Blocked") indicator="[!]" ;;
      *) indicator="[-]" ;;
    esac

    echo -n "$indicator $task"

    if [[ -n "$deps" ]]; then
      echo -n " <- {$deps}"
    fi

    echo ""

    # Show dependents indented
    if [[ -n "$dependents" ]]; then
      for dep in $dependents; do
        echo "    -> $dep"
      done
    fi
  done < <(deps_all_tasks)

  echo ""
  echo "Legend: [x]=Complete [>]=In Progress [?]=Review [ ]=Ready [!]=Blocked"
  echo ""
}

# Show recommended task order
deps_recommended_order() {
  echo ""
  echo "Recommended Task Order"
  echo "======================"
  echo ""

  local step=1
  while IFS= read -r task; do
    [[ -z "$task" ]] && continue

    local status=$(deps_compute_status "$task")
    local title=$(deps_get_title "$task")
    local deps=$(deps_get_deps "$task")

    # Skip completed tasks
    [[ "$status" == "Complete" ]] && continue

    if [[ -n "$deps" ]]; then
      printf "  %d. %-12s [%-11s] %s (after: %s)\n" "$step" "$task" "$status" "$title" "$deps"
    else
      printf "  %d. %-12s [%-11s] %s\n" "$step" "$task" "$status" "$title"
    fi
    step=$((step + 1))
  done < <(deps_all_tasks)

  echo ""
}

# Print summary
deps_summary() {
  echo ""
  echo "Dependency Analysis Summary"
  echo "==========================="
  echo ""

  local total=0
  local complete=0
  local in_progress=0
  local ready=0
  local blocked=0

  while IFS= read -r task; do
    [[ -z "$task" ]] && continue
    total=$((total + 1))

    local status=$(deps_compute_status "$task")
    case "$status" in
      "Complete") complete=$((complete + 1)) ;;
      "In Progress"|"In Review"|"Review") in_progress=$((in_progress + 1)) ;;
      "Ready") ready=$((ready + 1)) ;;
      "Blocked") blocked=$((blocked + 1)) ;;
    esac
  done < <(deps_all_tasks)

  echo "Total tasks:  $total"
  echo "Complete:     $complete"
  echo "In Progress:  $in_progress"
  echo "Ready:        $ready"
  echo "Blocked:      $blocked"
  echo ""

  # Check for cycles
  if ! deps_check_cycles >/dev/null 2>&1; then
    echo "WARNING: Circular dependencies detected!"
    deps_check_cycles
  else
    echo "No circular dependencies"
  fi

  echo ""
}

# Main entry point for CLI usage
deps_main() {
  local cmd="${1:-help}"
  shift || true

  case "$cmd" in
    build)
      deps_build_graph
      echo "Graph built: $(deps_all_tasks | wc -l | tr -d ' ') tasks"
      ;;
    cycles)
      deps_build_graph
      deps_check_cycles
      ;;
    validate)
      deps_build_graph
      deps_validate "$@"
      ;;
    blockers)
      deps_build_graph
      deps_get_blockers "$1"
      ;;
    dependents)
      deps_build_graph
      deps_get_dependents "$1"
      ;;
    status)
      deps_build_graph
      deps_compute_status "$1"
      ;;
    can-launch)
      deps_build_graph
      deps_can_launch "$1"
      ;;
    visualize|graph)
      deps_build_graph
      deps_visualize
      ;;
    order|recommended)
      deps_build_graph
      deps_recommended_order
      ;;
    summary|analyze)
      deps_build_graph
      deps_summary
      deps_visualize
      deps_recommended_order
      ;;
    help|--help|-h)
      echo "Usage: deps.sh <command> [args]"
      echo ""
      echo "Commands:"
      echo "  build              Build dependency graph from INDEX.md files"
      echo "  cycles             Check for circular dependencies"
      echo "  validate <id>      Validate that a dependency ID exists"
      echo "  blockers <id>      Get incomplete dependencies for a task"
      echo "  dependents <id>    Get tasks that depend on this one"
      echo "  status <id>        Compute effective status based on dependencies"
      echo "  can-launch <id>    Check if task can be launched"
      echo "  visualize          ASCII dependency graph"
      echo "  order              Show recommended task order"
      echo "  summary            Full dependency analysis"
      echo ""
      echo "Environment:"
      echo "  DEPS_VERBOSE=true  Enable debug logging"
      echo "  DEPS_CROSS_REPO=false  Disable cross-repo dependency scanning"
      ;;
    *)
      echo "Unknown command: $cmd"
      echo "Run 'deps.sh help' for usage"
      return 1
      ;;
  esac

  # Cleanup temp files
  deps_cleanup
}

# Run main if executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  deps_main "$@"
fi

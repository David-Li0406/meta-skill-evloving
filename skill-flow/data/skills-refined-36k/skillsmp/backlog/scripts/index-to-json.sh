#!/bin/bash
#
# index-to-json.sh - Parse INDEX.md into JSON format
#
# Outputs a JSON object with:
# - project: Project name from design.yaml or git repo
# - generated: Timestamp
# - tasks: Array of task objects
# - worktrees: Array of active worktree objects
# - summary: Status counts
#
# Usage:
#   ./index-to-json.sh              # Output to stdout
#   ./index-to-json.sh -o file.json # Output to file
#   ./index-to-json.sh --pretty     # Pretty-print JSON
#

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/deps.sh"

# Options
OUTPUT_FILE=""
PRETTY=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    -p|--pretty)
      PRETTY=true
      shift
      ;;
    -h|--help)
      echo "Usage: index-to-json.sh [options]"
      echo ""
      echo "Options:"
      echo "  -o, --output FILE  Write output to FILE instead of stdout"
      echo "  -p, --pretty       Pretty-print JSON output"
      echo "  -h, --help         Show this help"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

# Get project name
get_project_name() {
  local repo_root
  repo_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

  # Try design.yaml first
  if [[ -f "$repo_root/design.yaml" ]]; then
    local name
    name=$(grep "^project_name:" "$repo_root/design.yaml" 2>/dev/null | cut -d: -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    if [[ -n "$name" ]]; then
      echo "$name"
      return
    fi
    # Try repo_prefix as fallback
    name=$(grep "^repo_prefix:" "$repo_root/design.yaml" 2>/dev/null | cut -d: -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    if [[ -n "$name" ]]; then
      echo "$name"
      return
    fi
  fi

  # Fall back to git repo name
  basename "$repo_root"
}

# Get worktree information
get_worktrees() {
  local repo_root
  repo_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

  git worktree list --porcelain 2>/dev/null | while IFS= read -r line; do
    if [[ "$line" =~ ^worktree[[:space:]]+(.*) ]]; then
      local wt_path="${BASH_REMATCH[1]}"
      local branch=""
      local task_id=""
      local mode=""

      # Read next lines for branch
      read -r line || true
      if [[ "$line" =~ ^branch[[:space:]]+refs/heads/(.*) ]]; then
        branch="${BASH_REMATCH[1]}"
      fi

      # Skip main worktree
      [[ "$wt_path" == "$repo_root" ]] && continue

      # Check for PROMPT.md to get task ID
      if [[ -f "$wt_path/PROMPT.md" ]]; then
        task_id=$(grep -oE '^Task:[[:space:]]*([A-Z]+-[0-9]+)' "$wt_path/PROMPT.md" 2>/dev/null | head -1 | sed 's/Task:[[:space:]]*//' || true)
        # Check mode from PROMPT.md
        if grep -q "Code Review Mode" "$wt_path/PROMPT.md" 2>/dev/null; then
          mode="Code Review"
        else
          mode="Implementation"
        fi
      fi

      # Output as tab-separated for parsing
      echo -e "${wt_path}\t${branch}\t${task_id}\t${mode}"
    fi
  done
}

# Escape string for JSON
json_escape() {
  local str="$1"
  str="${str//\\/\\\\}"
  str="${str//\"/\\\"}"
  str="${str//$'\n'/\\n}"
  str="${str//$'\r'/\\r}"
  str="${str//$'\t'/\\t}"
  echo "$str"
}

# Build JSON output
build_json() {
  local project_name
  project_name=$(get_project_name)
  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  # Build dependency graph
  deps_build_graph

  # Collect worktree info into associative-like structure
  # Using temp file since bash 3.2 doesn't have associative arrays
  local wt_tmp
  wt_tmp=$(mktemp)
  get_worktrees > "$wt_tmp"

  # Start JSON
  echo "{"
  echo "  \"project\": \"$(json_escape "$project_name")\","
  echo "  \"generated\": \"$timestamp\","

  # Tasks array
  echo "  \"tasks\": ["

  local first_task=true
  local complete_count=0
  local in_progress_count=0
  local in_review_count=0
  local ready_count=0
  local blocked_count=0
  local complete_ids=""
  local in_progress_ids=""
  local in_review_ids=""
  local ready_ids=""
  local blocked_ids=""

  while IFS= read -r task_id; do
    [[ -z "$task_id" ]] && continue

    local title status computed_status deps blockers worktree_branch worktree_path worktree_mode
    title=$(deps_get_title "$task_id" || echo "")
    status=$(deps_get_status "$task_id" || echo "")
    computed_status=$(deps_compute_status "$task_id" || echo "")
    deps=$(deps_get_deps "$task_id" || echo "")
    blockers=$(deps_get_blockers "$task_id" || echo "")

    # Look up worktree info
    worktree_branch=""
    worktree_path=""
    worktree_mode=""
    while IFS=$'\t' read -r wt_path wt_branch wt_task wt_mode; do
      if [[ "$wt_task" == "$task_id" ]]; then
        worktree_path="$wt_path"
        worktree_branch="$wt_branch"
        worktree_mode="$wt_mode"
        break
      fi
    done < "$wt_tmp"

    # Count by computed status
    case "$computed_status" in
      "Complete")
        complete_count=$((complete_count + 1))
        complete_ids="${complete_ids:+$complete_ids, }$task_id"
        ;;
      "In Progress")
        in_progress_count=$((in_progress_count + 1))
        in_progress_ids="${in_progress_ids:+$in_progress_ids, }$task_id"
        ;;
      "In Review"|"Review"|"Changes Requested")
        in_review_count=$((in_review_count + 1))
        in_review_ids="${in_review_ids:+$in_review_ids, }$task_id"
        ;;
      "Ready")
        ready_count=$((ready_count + 1))
        ready_ids="${ready_ids:+$ready_ids, }$task_id"
        ;;
      "Blocked")
        blocked_count=$((blocked_count + 1))
        blocked_ids="${blocked_ids:+$blocked_ids, }$task_id"
        ;;
    esac

    # Output task JSON
    if [[ "$first_task" == "false" ]]; then
      echo ","
    fi
    first_task=false

    # Convert deps and blockers to JSON arrays
    local deps_json
    local blockers_json
    deps_json="[]"
    blockers_json="[]"
    if [[ -n "${deps:-}" ]]; then
      deps_json="[$(echo "$deps" | tr ' ' '\n' | sed 's/.*/"&"/' | tr '\n' ',' | sed 's/,$//')"]"
    fi
    if [[ -n "${blockers:-}" ]]; then
      blockers_json="[$(echo "$blockers" | tr ' ' '\n' | sed 's/.*/"&"/' | tr '\n' ',' | sed 's/,$//')"]"
    fi

    echo -n "    {"
    echo -n "\"id\": \"$(json_escape "$task_id")\", "
    echo -n "\"title\": \"$(json_escape "${title:-}")\", "
    echo -n "\"status\": \"$(json_escape "${status:-}")\", "
    echo -n "\"computedStatus\": \"$(json_escape "${computed_status:-}")\", "
    echo -n "\"dependencies\": $deps_json, "
    echo -n "\"blockers\": $blockers_json, "
    echo -n "\"worktree\": {"
    echo -n "\"branch\": $(if [[ -n "$worktree_branch" ]]; then echo "\"$(json_escape "$worktree_branch")\""; else echo "null"; fi), "
    echo -n "\"path\": $(if [[ -n "$worktree_path" ]]; then echo "\"$(json_escape "$worktree_path")\""; else echo "null"; fi), "
    echo -n "\"mode\": $(if [[ -n "$worktree_mode" ]]; then echo "\"$(json_escape "$worktree_mode")\""; else echo "null"; fi)"
    echo -n "}"
    echo -n "}"
  done < <(deps_all_tasks)

  echo ""
  echo "  ],"

  # Worktrees array (all active worktrees, including orphans)
  echo "  \"worktrees\": ["
  local first_wt=true
  while IFS=$'\t' read -r wt_path wt_branch wt_task wt_mode; do
    [[ -z "$wt_path" ]] && continue

    if [[ "$first_wt" == "false" ]]; then
      echo ","
    fi
    first_wt=false

    echo -n "    {"
    echo -n "\"path\": \"$(json_escape "$wt_path")\", "
    echo -n "\"branch\": \"$(json_escape "$wt_branch")\", "
    echo -n "\"taskId\": $(if [[ -n "$wt_task" ]]; then echo "\"$(json_escape "$wt_task")\""; else echo "null"; fi), "
    echo -n "\"mode\": $(if [[ -n "$wt_mode" ]]; then echo "\"$(json_escape "$wt_mode")\""; else echo "null"; fi)"
    echo -n "}"
  done < "$wt_tmp"
  echo ""
  echo "  ],"

  # Summary
  local total=$((complete_count + in_progress_count + in_review_count + ready_count + blocked_count))
  echo "  \"summary\": {"
  echo "    \"total\": $total,"
  echo "    \"byStatus\": {"
  echo "      \"complete\": {\"count\": $complete_count, \"tasks\": \"$complete_ids\"},"
  echo "      \"inProgress\": {\"count\": $in_progress_count, \"tasks\": \"$in_progress_ids\"},"
  echo "      \"inReview\": {\"count\": $in_review_count, \"tasks\": \"$in_review_ids\"},"
  echo "      \"ready\": {\"count\": $ready_count, \"tasks\": \"$ready_ids\"},"
  echo "      \"blocked\": {\"count\": $blocked_count, \"tasks\": \"$blocked_ids\"}"
  echo "    }"
  echo "  }"
  echo "}"

  # Cleanup
  rm -f "$wt_tmp"
  deps_cleanup
}

# Main
main() {
  local json
  json=$(build_json)

  # Pretty print if requested and jq is available
  if [[ "$PRETTY" == "true" ]] && command -v jq &>/dev/null; then
    json=$(echo "$json" | jq .)
  fi

  if [[ -n "$OUTPUT_FILE" ]]; then
    echo "$json" > "$OUTPUT_FILE"
    echo "Written to $OUTPUT_FILE" >&2
  else
    echo "$json"
  fi
}

main

#!/bin/bash
#
# format-task-list.sh - Format task JSON into beautiful terminal output
#
# Reads JSON from stdin or file and outputs a formatted task table
# with status emojis, summaries, and actionable next steps.
#
# Usage:
#   ./index-to-json.sh | ./format-task-list.sh
#   ./format-task-list.sh < tasks.json
#   ./format-task-list.sh -f tasks.json
#   ./format-task-list.sh --no-color  # Disable colors
#   ./format-task-list.sh --compact   # Minimal output
#

set -euo pipefail

# Options
INPUT_FILE=""
NO_COLOR=false
COMPACT=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -f|--file)
      INPUT_FILE="$2"
      shift 2
      ;;
    --no-color)
      NO_COLOR=true
      shift
      ;;
    --compact)
      COMPACT=true
      shift
      ;;
    -h|--help)
      echo "Usage: format-task-list.sh [options]"
      echo ""
      echo "Options:"
      echo "  -f, --file FILE  Read JSON from FILE instead of stdin"
      echo "  --no-color       Disable color output"
      echo "  --compact        Minimal output (just the task table)"
      echo "  -h, --help       Show this help"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

# Status emoji mapping
get_status_emoji() {
  local status="$1"
  case "$status" in
    "Complete") echo "✅" ;;
    "In Progress") echo "🚀" ;;
    "In Review"|"Review") echo "📋" ;;
    "Changes Requested") echo "🔄" ;;
    "Ready") echo "🆕" ;;
    "Blocked") echo "❌" ;;
    *) echo "❓" ;;
  esac
}

# Format status with emoji
format_status() {
  local status="$1"
  local emoji
  emoji=$(get_status_emoji "$status")
  echo "$emoji $status"
}

# Calculate string display width (accounting for emojis as 2 chars)
str_width() {
  local str="$1"
  local len=${#str}
  # Count emojis (rough approximation - emojis are typically 3-4 bytes in UTF-8)
  local emoji_count
  emoji_count=$(echo "$str" | grep -o '[✅🚀📋🔄🆕❌❓]' | wc -l | tr -d ' ')
  # Emojis display as ~2 chars wide, but take 1 char in string length
  echo $((len + emoji_count))
}

# Pad string to width
pad_string() {
  local str="$1"
  local target_width="$2"
  local current_width
  current_width=$(str_width "$str")
  local padding=$((target_width - current_width))
  if [[ $padding -gt 0 ]]; then
    printf "%s%*s" "$str" "$padding" ""
  else
    echo "$str"
  fi
}

# Draw horizontal line
draw_line() {
  local left="$1"
  local mid="$2"
  local right="$3"
  shift 3
  local widths=("$@")
  local line="$left"
  local first=true
  for w in "${widths[@]}"; do
    if [[ "$first" != "true" ]]; then
      line+="$mid"
    fi
    first=false
    line+=$(printf '%*s' "$((w + 2))" '' | tr ' ' '─')
  done
  line+="$right"
  echo "$line"
}

# Read JSON
read_json() {
  if [[ -n "$INPUT_FILE" ]]; then
    cat "$INPUT_FILE"
  else
    cat
  fi
}

# Main formatting function
format_output() {
  local json
  json=$(read_json)

  # Check if jq is available
  if ! command -v jq &>/dev/null; then
    echo "Error: jq is required for formatting. Install with: brew install jq" >&2
    exit 1
  fi

  # Extract data
  local project
  project=$(echo "$json" | jq -r '.project // "Unknown"')

  # Calculate column widths
  local id_width=8
  local title_width=10
  local status_width=16
  local deps_width=12
  local wt_width=10

  # First pass: calculate max widths
  while IFS= read -r task; do
    local id title status deps wt
    id=$(echo "$task" | jq -r '.id')
    title=$(echo "$task" | jq -r '.title')
    status=$(format_status "$(echo "$task" | jq -r '.computedStatus')")
    deps=$(echo "$task" | jq -r '.dependencies | if length == 0 then "-" else join(", ") end')
    wt=$(echo "$task" | jq -r '.worktree.branch // "-"')

    [[ ${#id} -gt $id_width ]] && id_width=${#id}
    [[ ${#title} -gt $title_width ]] && title_width=${#title}
    local sw; sw=$(str_width "$status")
    [[ $sw -gt $status_width ]] && status_width=$sw
    [[ ${#deps} -gt $deps_width ]] && deps_width=${#deps}
    [[ ${#wt} -gt $wt_width ]] && wt_width=${#wt}
  done < <(echo "$json" | jq -c '.tasks[]')

  # Cap widths for readability
  [[ $title_width -gt 40 ]] && title_width=40
  [[ $deps_width -gt 24 ]] && deps_width=24
  [[ $wt_width -gt 28 ]] && wt_width=28

  local widths=($id_width $title_width $status_width $deps_width $wt_width)

  # Header
  if [[ "$COMPACT" != "true" ]]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  TASK LIST: $project"
    echo "═══════════════════════════════════════════════════════════════════════════════"
  fi

  # Task table
  echo "$(draw_line "┌" "┬" "┐" "${widths[@]}")"

  # Header row
  printf "│ %s │ %s │ %s │ %s │ %s │\n" \
    "$(pad_string "ID" $id_width)" \
    "$(pad_string "Title" $title_width)" \
    "$(pad_string "Status" $status_width)" \
    "$(pad_string "Dependencies" $deps_width)" \
    "$(pad_string "Worktree" $wt_width)"

  echo "$(draw_line "├" "┼" "┤" "${widths[@]}")"

  # Data rows
  local first_row=true
  while IFS= read -r task; do
    local id title status deps wt
    id=$(echo "$task" | jq -r '.id')
    title=$(echo "$task" | jq -r '.title')
    # Truncate title if too long
    if [[ ${#title} -gt $title_width ]]; then
      title="${title:0:$((title_width-3))}..."
    fi
    status=$(format_status "$(echo "$task" | jq -r '.computedStatus')")
    deps=$(echo "$task" | jq -r '.dependencies | if length == 0 then "-" else join(", ") end')
    if [[ ${#deps} -gt $deps_width ]]; then
      deps="${deps:0:$((deps_width-3))}..."
    fi
    wt=$(echo "$task" | jq -r '.worktree.branch // "-"')
    if [[ ${#wt} -gt $wt_width ]]; then
      wt="${wt:0:$((wt_width-3))}..."
    fi

    if [[ "$first_row" != "true" ]]; then
      echo "$(draw_line "├" "┼" "┤" "${widths[@]}")"
    fi
    first_row=false

    printf "│ %s │ %s │ %s │ %s │ %s │\n" \
      "$(pad_string "$id" $id_width)" \
      "$(pad_string "$title" $title_width)" \
      "$(pad_string "$status" $status_width)" \
      "$(pad_string "$deps" $deps_width)" \
      "$(pad_string "$wt" $wt_width)"
  done < <(echo "$json" | jq -c '.tasks[]')

  echo "$(draw_line "└" "┴" "┘" "${widths[@]}")"

  # Compact mode stops here
  if [[ "$COMPACT" == "true" ]]; then
    return
  fi

  # Summary section
  echo ""
  echo "Summary"
  echo ""
  local total
  total=$(echo "$json" | jq -r '.summary.total')
  echo "Total: $total tasks"

  # Status summary table
  local sum_status_width=16
  local sum_count_width=5
  local sum_tasks_width=30
  local sum_widths=($sum_status_width $sum_count_width $sum_tasks_width)

  echo "$(draw_line "┌" "┬" "┐" "${sum_widths[@]}")"
  printf "│ %s │ %s │ %s │\n" \
    "$(pad_string "Status" $sum_status_width)" \
    "$(pad_string "Count" $sum_count_width)" \
    "$(pad_string "Tasks" $sum_tasks_width)"
  echo "$(draw_line "├" "┼" "┤" "${sum_widths[@]}")"

  local first_sum=true
  for status_key in complete inProgress inReview ready blocked; do
    local count tasks status_display
    count=$(echo "$json" | jq -r ".summary.byStatus.$status_key.count")
    tasks=$(echo "$json" | jq -r ".summary.byStatus.$status_key.tasks")

    [[ "$count" == "0" ]] && continue

    case "$status_key" in
      complete) status_display="✅ Complete" ;;
      inProgress) status_display="🚀 In Progress" ;;
      inReview) status_display="📋 In Review" ;;
      ready) status_display="🆕 Ready" ;;
      blocked) status_display="❌ Blocked" ;;
    esac

    # Truncate tasks if too long
    if [[ ${#tasks} -gt $sum_tasks_width ]]; then
      tasks="${tasks:0:$((sum_tasks_width-3))}..."
    fi

    if [[ "$first_sum" != "true" ]]; then
      echo "$(draw_line "├" "┼" "┤" "${sum_widths[@]}")"
    fi
    first_sum=false

    printf "│ %s │ %s │ %s │\n" \
      "$(pad_string "$status_display" $sum_status_width)" \
      "$(pad_string "$count" $sum_count_width)" \
      "$(pad_string "$tasks" $sum_tasks_width)"
  done
  echo "$(draw_line "└" "┴" "┘" "${sum_widths[@]}")"

  # Active worktrees section
  local wt_count
  wt_count=$(echo "$json" | jq '.worktrees | length')
  if [[ "$wt_count" -gt 0 ]]; then
    echo ""
    echo "Active Worktrees"

    local wt_task_width=8
    local wt_branch_width=28
    local wt_path_width=60
    local wt_mode_width=14
    local wt_widths=($wt_task_width $wt_branch_width $wt_path_width $wt_mode_width)

    echo "$(draw_line "┌" "┬" "┐" "${wt_widths[@]}")"
    printf "│ %s │ %s │ %s │ %s │\n" \
      "$(pad_string "Task" $wt_task_width)" \
      "$(pad_string "Branch" $wt_branch_width)" \
      "$(pad_string "Path" $wt_path_width)" \
      "$(pad_string "Mode" $wt_mode_width)"
    echo "$(draw_line "├" "┼" "┤" "${wt_widths[@]}")"

    local first_wt=true
    while IFS= read -r wt; do
      local wt_task wt_branch wt_path wt_mode
      wt_task=$(echo "$wt" | jq -r '.taskId // "-"')
      wt_branch=$(echo "$wt" | jq -r '.branch')
      wt_path=$(echo "$wt" | jq -r '.path')
      wt_mode=$(echo "$wt" | jq -r '.mode // "-"')

      # Truncate if needed
      [[ ${#wt_branch} -gt $wt_branch_width ]] && wt_branch="${wt_branch:0:$((wt_branch_width-3))}..."
      [[ ${#wt_path} -gt $wt_path_width ]] && wt_path="${wt_path:0:$((wt_path_width-3))}..."

      if [[ "$first_wt" != "true" ]]; then
        echo "$(draw_line "├" "┼" "┤" "${wt_widths[@]}")"
      fi
      first_wt=false

      printf "│ %s │ %s │ %s │ %s │\n" \
        "$(pad_string "$wt_task" $wt_task_width)" \
        "$(pad_string "$wt_branch" $wt_branch_width)" \
        "$(pad_string "$wt_path" $wt_path_width)" \
        "$(pad_string "$wt_mode" $wt_mode_width)"
    done < <(echo "$json" | jq -c '.worktrees[]')
    echo "$(draw_line "└" "┴" "┘" "${wt_widths[@]}")"
  fi

  # Next Actions section
  echo ""
  echo "Next Actions"
  echo ""

  # Ready to start
  local ready_tasks
  ready_tasks=$(echo "$json" | jq -r '.tasks[] | select(.computedStatus == "Ready") | "- /backlog:launch \(.id) - \(.title)"')
  if [[ -n "$ready_tasks" ]]; then
    echo "Ready to start:"
    echo "$ready_tasks"
    echo ""
  fi

  # Currently blocked
  local blocked_info
  blocked_info=$(echo "$json" | jq -r '.tasks[] | select(.computedStatus == "Blocked") | "- \(.id): Waiting on \(.blockers | join(", "))"')
  if [[ -n "$blocked_info" ]]; then
    echo "Currently blocked:"
    echo "$blocked_info"
    echo ""
  fi
}

format_output

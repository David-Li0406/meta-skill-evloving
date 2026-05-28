#!/bin/bash
# Plan - Plan Directory & Listing
#
# Usage:
#   plan dir                          Show plans directory path
#   plan list [--status <status>]     List all plans
#   plan resolve <identifier>         Resolve plan path from identifier

set -e

# Source common functions
source "$(dirname "$0")/../_common.sh"

# Check project initialization
check_project_initialized

COMMAND="$1"
PLANS_DIR="$BLUEPRINT_DATA_DIR/plans"

# =============================================================================
# Commands
# =============================================================================

do_dir() {
  echo "$PLANS_DIR"
}

do_list() {
  local status_filter=""

  # Parse --status flag
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --status|-s)
        status_filter="$2"
        shift 2
        ;;
      *)
        shift
        ;;
    esac
  done

  if [ ! -d "$PLANS_DIR" ]; then
    error "Plans directory not found: $PLANS_DIR"
    exit 1
  fi

  # List plan directories
  local found=0
  for plan_dir in "$PLANS_DIR"/*/; do
    [ -d "$plan_dir" ] || continue
    local plan_name
    plan_name=$(basename "$plan_dir")

    # If status filter, check PLAN.md frontmatter
    if [ -n "$status_filter" ]; then
      local plan_file="$plan_dir/PLAN.md"
      if [ -f "$plan_file" ]; then
        local fm
        fm=$(get_frontmatter "$plan_file")
        local plan_status
        plan_status=$(get_field "$fm" "status")
        [ "$plan_status" != "$status_filter" ] && continue
      else
        # No PLAN.md, skip if filtering
        continue
      fi
    fi

    echo "$plan_name"
    found=1
  done

  if [ "$found" -eq 0 ]; then
    if [ -n "$status_filter" ]; then
      info "No plans found with status: $status_filter"
    else
      info "No plans found in $PLANS_DIR"
    fi
  fi
}

do_resolve() {
  local identifier="$1"

  if [ -z "$identifier" ]; then
    echo "Usage: plan resolve <identifier>"
    echo ""
    echo "Identifier formats:"
    echo "  001        matches {PLANS_DIR}/001-*/"
    echo "  auth       matches {PLANS_DIR}/*-*auth*/"
    echo "  001-auth   matches {PLANS_DIR}/001-auth*/"
    exit 1
  fi

  if [ ! -d "$PLANS_DIR" ]; then
    error "Plans directory not found: $PLANS_DIR"
    exit 1
  fi

  local matches=()

  # Pattern matching based on identifier format
  if [[ "$identifier" =~ ^[0-9]+$ ]]; then
    # Number only: 001 → 001-*/
    for d in "$PLANS_DIR"/${identifier}-*/; do
      [ -d "$d" ] && matches+=("$d")
    done
  elif [[ "$identifier" =~ ^[0-9]+-(.+)$ ]]; then
    # Full format: 001-auth → 001-auth*/
    for d in "$PLANS_DIR"/${identifier}*/; do
      [ -d "$d" ] && matches+=("$d")
    done
  else
    # Text only: auth → *-*auth*/
    for d in "$PLANS_DIR"/*-*${identifier}*/; do
      [ -d "$d" ] && matches+=("$d")
    done
  fi

  if [ ${#matches[@]} -eq 0 ]; then
    error "No plan found matching: $identifier"
    echo ""
    echo "Available plans:"
    do_list
    exit 1
  elif [ ${#matches[@]} -gt 1 ]; then
    error "Multiple plans match '$identifier':"
    for m in "${matches[@]}"; do
      echo "  - $(basename "$m")"
    done
    echo ""
    echo "Please be more specific."
    exit 1
  fi

  # Return path without trailing slash
  echo "${matches[0]%/}"
}

# =============================================================================
# Main Dispatch
# =============================================================================

case "$COMMAND" in
  dir)
    do_dir
    ;;
  list)
    shift
    do_list "$@"
    ;;
  resolve)
    shift
    do_resolve "$@"
    ;;
  -h|--help|"")
    echo "Plan - Plan Directory & Listing"
    echo ""
    echo "Usage:"
    echo "  plan dir                          Show plans directory path"
    echo "  plan list [--status <status>]     List all plans"
    echo "  plan resolve <identifier>         Resolve plan path"
    echo ""
    echo "Options:"
    echo "  -h, --help    Show this help message"
    echo ""
    echo "Examples:"
    echo "  blueprint.sh plan dir"
    echo "  blueprint.sh plan list"
    echo "  blueprint.sh plan list --status in-progress"
    echo "  blueprint.sh plan resolve 001"
    echo "  blueprint.sh plan resolve auth"
    exit 1
    ;;
  *)
    error "Unknown command: $COMMAND"
    echo ""
    echo "Run 'blueprint.sh plan --help' for usage."
    exit 1
    ;;
esac

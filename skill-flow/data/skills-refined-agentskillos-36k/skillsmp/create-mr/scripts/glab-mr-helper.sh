#!/bin/bash
# Helper script for glab API operations during MR creation.
# This script is intended to be allow-listed in Claude settings to avoid
# repeated permission prompts for glab api commands.

set -euo pipefail

usage() {
    cat <<EOF
Usage: $(basename "$0") <command> [args...]

Commands:
  project-id                      Get the current project ID
  find-mr-by-source <branch>      Find open MR with given source branch
  set-blocking <mr-iid> <target>  Set up blocking dependency for stacked MR
  help                            Show this help

Examples:
  $(basename "$0") project-id
  $(basename "$0") find-mr-by-source feature/parent-branch
  $(basename "$0") set-blocking 123 feature/parent-branch
EOF
}

get_project_id() {
    glab repo view --output json | jq -r '.id'
}

find_mr_by_source() {
    local source_branch="$1"
    local project_id
    project_id=$(get_project_id)

    # URL-encode the branch name
    local encoded_branch
    encoded_branch=$(printf '%s' "$source_branch" | jq -sRr @uri)

    # Find open MR with this source branch
    glab api "projects/${project_id}/merge_requests?state=opened&source_branch=${encoded_branch}" | \
        jq -r '.[0].iid // empty'
}

set_blocking() {
    local mr_iid="$1"
    local target_branch="$2"

    local project_id
    project_id=$(get_project_id)

    # Find the parent MR (whose source branch = our target branch)
    local parent_mr_iid
    parent_mr_iid=$(find_mr_by_source "$target_branch")

    if [[ -z "$parent_mr_iid" ]]; then
        echo "No open MR found with source branch '$target_branch'" >&2
        exit 1
    fi

    echo "Found parent MR !${parent_mr_iid} (source: ${target_branch})"
    echo "Setting !${parent_mr_iid} as blocking for !${mr_iid}..."

    # Create blocking relationship: parent blocks this MR
    glab api -X POST "projects/${project_id}/merge_requests/${mr_iid}/blocks?blocking_merge_request_id=${parent_mr_iid}" \
        --silent > /dev/null

    echo "Done. MR !${mr_iid} is now blocked by !${parent_mr_iid}"
}

# Main dispatch
case "${1:-help}" in
    project-id)
        get_project_id
        ;;
    find-mr-by-source)
        if [[ -z "${2:-}" ]]; then
            echo "Error: branch name required" >&2
            exit 1
        fi
        find_mr_by_source "$2"
        ;;
    set-blocking)
        if [[ -z "${2:-}" ]] || [[ -z "${3:-}" ]]; then
            echo "Error: mr-iid and target-branch required" >&2
            exit 1
        fi
        set_blocking "$2" "$3"
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        echo "Unknown command: $1" >&2
        usage >&2
        exit 1
        ;;
esac

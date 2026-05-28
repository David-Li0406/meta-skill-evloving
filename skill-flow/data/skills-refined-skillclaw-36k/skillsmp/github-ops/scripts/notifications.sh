#!/usr/bin/env bash
#
# notifications.sh - Notification Operations for GitHub Ops Skill
# MCP Parity: list_notifications, mark_notification_read, get_notification_thread
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

LIMIT=30
JSON_OUTPUT=false

usage() {
    cat << EOF
Usage: $(basename "$0") <action> [options]

Notification Operations - GitHub MCP Server Parity

Actions:
  list              List notifications
  thread            View a notification thread
  mark-read         Mark notification(s) as read
  mark-all-read     Mark all notifications as read
  subscribe         Subscribe to a thread
  unsubscribe       Unsubscribe from a thread

Common Options:
  --id ID           Thread ID (for thread/mark-read/subscribe)
  --owner OWNER     Filter by repository owner
  --repo REPO       Filter by repository name
  --all             Include read notifications
  --participating   Only participating notifications
  --limit N         Maximum results (default: 30)
  --json            Output in JSON format
  --help            Show this help message

Examples:
  $(basename "$0") list --limit 10
  $(basename "$0") list --owner cli --repo cli
  $(basename "$0") thread --id 12345678
  $(basename "$0") mark-read --id 12345678
  $(basename "$0") mark-all-read --owner cli --repo cli
EOF
    exit 0
}

error() { echo -e "${RED}Error: $1${NC}" >&2; exit 1; }
info() { echo -e "${BLUE}$1${NC}"; }
success() { echo -e "${GREEN}$1${NC}"; }
warn() { echo -e "${YELLOW}$1${NC}"; }

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --id) THREAD_ID="$2"; shift 2 ;;
            --owner) OWNER="$2"; shift 2 ;;
            --repo) REPO="$2"; shift 2 ;;
            --all) ALL=true; shift ;;
            --participating) PARTICIPATING=true; shift ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --json) JSON_OUTPUT=true; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

# Action: List notifications
action_list() {
    info "Listing notifications"
    
    local params="per_page=$LIMIT"
    [[ "${ALL:-false}" == "true" ]] && params="$params&all=true"
    [[ "${PARTICIPATING:-false}" == "true" ]] && params="$params&participating=true"
    
    local endpoint="notifications?$params"
    
    # If owner/repo specified, filter to that repo
    if [[ -n "${OWNER:-}" ]] && [[ -n "${REPO:-}" ]]; then
        endpoint="repos/$OWNER/$REPO/notifications?$params"
    fi
    
    local result
    result=$(gh api "$endpoint" 2>&1) || {
        error "Failed to fetch notifications"
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result"
    else
        local count
        count=$(echo "$result" | jq 'length')
        if [[ "$count" == "0" ]]; then
            echo "No notifications found."
            return 0
        fi
        
        echo "$result" | jq -r '.[] | 
            "\(.id)\t\(.repository.full_name)\t\(.subject.type)\t\(.subject.title | .[0:50])\t\(.reason)\t\(.updated_at)"' \
            | column -t -s $'\t'
    fi
}

# Action: View a notification thread
action_thread() {
    [[ -z "${THREAD_ID:-}" ]] && error "Missing --id"
    
    info "Fetching notification thread $THREAD_ID"
    
    local result
    result=$(gh api "notifications/threads/$THREAD_ID" 2>&1) || {
        error "Failed to fetch thread $THREAD_ID"
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result"
    else
        echo "$result" | jq -r '"
Thread ID: \(.id)
Repository: \(.repository.full_name)
Type: \(.subject.type)
Title: \(.subject.title)
Reason: \(.reason)
Unread: \(.unread)
Updated: \(.updated_at)
URL: \(.subject.url // "N/A")"'
    fi
}

# Action: Mark notification as read
action_mark_read() {
    [[ -z "${THREAD_ID:-}" ]] && error "Missing --id"
    
    info "Marking notification $THREAD_ID as read"
    
    gh api "notifications/threads/$THREAD_ID" -X PATCH >/dev/null 2>&1 || {
        error "Failed to mark notification as read"
    }
    
    success "Notification $THREAD_ID marked as read"
}

# Action: Mark all notifications as read
action_mark_all_read() {
    if [[ -n "${OWNER:-}" ]] && [[ -n "${REPO:-}" ]]; then
        info "Marking all notifications as read for $OWNER/$REPO"
        gh api "repos/$OWNER/$REPO/notifications" -X PUT -f read=true >/dev/null 2>&1 || {
            error "Failed to mark notifications as read"
        }
        success "All notifications for $OWNER/$REPO marked as read"
    else
        info "Marking all notifications as read"
        gh api "notifications" -X PUT -f read=true >/dev/null 2>&1 || {
            error "Failed to mark notifications as read"
        }
        success "All notifications marked as read"
    fi
}

# Action: Subscribe to a thread
action_subscribe() {
    [[ -z "${THREAD_ID:-}" ]] && error "Missing --id"
    
    info "Subscribing to thread $THREAD_ID"
    
    gh api "notifications/threads/$THREAD_ID/subscription" \
        -X PUT -f subscribed=true -f ignored=false >/dev/null 2>&1 || {
        error "Failed to subscribe to thread"
    }
    
    success "Subscribed to thread $THREAD_ID"
}

# Action: Unsubscribe from a thread
action_unsubscribe() {
    [[ -z "${THREAD_ID:-}" ]] && error "Missing --id"
    
    info "Unsubscribing from thread $THREAD_ID"
    
    gh api "notifications/threads/$THREAD_ID/subscription" -X DELETE >/dev/null 2>&1 || {
        error "Failed to unsubscribe from thread"
    }
    
    success "Unsubscribed from thread $THREAD_ID"
}

main() {
    [[ $# -eq 0 ]] && usage
    local action="$1"; shift
    parse_args "$@"
    
    case "$action" in
        list) action_list ;;
        thread) action_thread ;;
        mark-read) action_mark_read ;;
        mark-all-read) action_mark_all_read ;;
        subscribe) action_subscribe ;;
        unsubscribe) action_unsubscribe ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action" ;;
    esac
}

main "$@"

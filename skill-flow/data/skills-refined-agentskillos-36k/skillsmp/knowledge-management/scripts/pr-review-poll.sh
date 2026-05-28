#!/bin/bash
# PR Review Polling Daemon
# Polls GitHub for PR review updates and notifies user
#
# Usage: ./pr-review-poll.sh [options]
# Options:
#   --interval N     Polling interval in seconds (default: 300 = 5 minutes)
#   --once           Run once and exit (for testing)
#   --repo OWNER/REPO  Specific repo (default: current repo)
#   -h, --help       Show this help message

set -euo pipefail

# Default configuration
POLL_INTERVAL=300  # 5 minutes
RUN_ONCE=false
REPO=""
AUTO_RESPOND=false
WORKING_DIR=""
INCLUDE_COPILOT=true  # Include Copilot reviews by default
STATE_FILE="${HOME}/.pr-review-state.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copilot reviewer username
COPILOT_REVIEWER="copilot-pull-request-reviewer"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Sanitize string for AppleScript (escape quotes and backslashes)
sanitize_for_applescript() {
    local str="$1"
    # Escape backslashes first, then double quotes
    str="${str//\\/\\\\}"
    str="${str//\"/\\\"}"
    echo "$str"
}

# Help message
show_help() {
    cat << EOF
PR Review Polling Daemon

Polls GitHub for PR review updates and sends notifications when:
- A PR receives a new review
- A review decision changes (approved, changes requested)
- New review comments are added

Usage: ./pr-review-poll.sh [options]

Options:
  --interval N       Polling interval in seconds (default: 300 = 5 minutes)
  --once             Run once and exit (useful for testing)
  --repo OWNER/REPO  Specific repo to monitor (default: current directory's repo)
  --auto-respond     Automatically spawn Claude CLI to handle reviews
  --working-dir DIR  Working directory for Claude CLI (required with --auto-respond)
  --include-copilot  Include Copilot reviews (default: enabled)
  --no-copilot       Exclude Copilot reviews from notifications
  -h, --help         Show this help message

State:
  Review state is stored in: $STATE_FILE

Examples:
  ./pr-review-poll.sh                     # Start daemon with defaults
  ./pr-review-poll.sh --interval 60       # Poll every minute
  ./pr-review-poll.sh --once              # Check once and exit
  ./pr-review-poll.sh --repo user/repo    # Monitor specific repo

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --interval)
            POLL_INTERVAL="$2"
            shift 2
            ;;
        --once)
            RUN_ONCE=true
            shift
            ;;
        --repo)
            REPO="$2"
            shift 2
            ;;
        --auto-respond)
            AUTO_RESPOND=true
            shift
            ;;
        --working-dir)
            WORKING_DIR="$2"
            shift 2
            ;;
        --include-copilot)
            INCLUDE_COPILOT=true
            shift
            ;;
        --no-copilot)
            INCLUDE_COPILOT=false
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Validate auto-respond requirements
if [[ "$AUTO_RESPOND" == "true" ]]; then
    if [[ -z "$WORKING_DIR" ]]; then
        echo -e "${RED}Error: --working-dir is required when using --auto-respond${NC}"
        exit 1
    fi
    if [[ ! -d "$WORKING_DIR" ]]; then
        echo -e "${RED}Error: Working directory does not exist: $WORKING_DIR${NC}"
        exit 1
    fi
    if ! command -v claude &> /dev/null; then
        echo -e "${RED}Error: Claude CLI not found. Please install Claude Code.${NC}"
        exit 1
    fi
fi

# Get repo from git if not specified
if [[ -z "$REPO" ]]; then
    REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null || echo "")
    if [[ -z "$REPO" ]]; then
        echo -e "${RED}Error: Could not determine repository. Use --repo flag or run from a git repo.${NC}"
        exit 1
    fi
fi

# Ensure state file exists
if [[ ! -f "$STATE_FILE" ]]; then
    echo '{}' > "$STATE_FILE"
fi

# Spawn Claude CLI to handle PR review
spawn_claude_pr_review() {
    local pr_number="$1"
    local pr_title="$2"
    local reviewer="$3"
    local review_state="$4"

    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} Spawning Claude CLI for PR #$pr_number..."

    # Create log file for this session
    local log_file="${HOME}/.pr-review-claude-${pr_number}-$(date '+%Y%m%d-%H%M%S').log"

    # Build the prompt
    local prompt="Review feedback received on PR #${pr_number} from @${reviewer} (${review_state}). Please run /pr-review ${pr_number} to analyze and respond to the feedback."

    # Spawn Claude CLI in the working directory
    # Using nohup to run in background, output to log file
    (
        cd "$WORKING_DIR"
        echo "=== Claude PR Review Session ===" > "$log_file"
        echo "PR: #$pr_number - $pr_title" >> "$log_file"
        echo "Reviewer: @$reviewer" >> "$log_file"
        echo "State: $review_state" >> "$log_file"
        echo "Started: $(date)" >> "$log_file"
        echo "Working Dir: $WORKING_DIR" >> "$log_file"
        echo "================================" >> "$log_file"
        echo "" >> "$log_file"

        # Find Claude CLI - check multiple locations
        local claude_cmd=""
        if [[ -x "${HOME}/.asdf/installs/nodejs/22.14.0/bin/claude" ]]; then
            claude_cmd="${HOME}/.asdf/installs/nodejs/22.14.0/bin/claude"
        elif command -v claude &> /dev/null; then
            claude_cmd="claude"
        else
            echo "ERROR: Claude CLI not found" >> "$log_file"
            exit 1
        fi

        echo "Using Claude: $claude_cmd" >> "$log_file"

        # Run Claude CLI with the prompt
        # --print outputs result without interactive mode
        # --permission-mode bypassPermissions to avoid blocking on permission prompts
        "$claude_cmd" --print --permission-mode bypassPermissions "$prompt" >> "$log_file" 2>&1

        echo "" >> "$log_file"
        echo "=== Session Complete ===" >> "$log_file"
        echo "Ended: $(date)" >> "$log_file"
    ) &

    local claude_pid=$!
    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} Claude spawned (PID: $claude_pid)"
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} Log file: $log_file"
}

# Send notification
send_notification() {
    local pr_number="$1"
    local pr_title="$2"
    local reviewer="$3"
    local review_state="$4"

    local title="PR Review: #${pr_number}"
    local message=""
    local sound="Ping"

    case "$review_state" in
        APPROVED)
            message="Approved by @${reviewer}"
            sound="Glass"
            ;;
        CHANGES_REQUESTED)
            message="Changes requested by @${reviewer}"
            sound="Basso"
            ;;
        COMMENTED)
            message="@${reviewer} left a comment"
            sound="Ping"
            ;;
        *)
            message="Reviewed by @${reviewer}"
            sound="Ping"
            ;;
    esac

    # Add suggestion to run /pr-review
    message="${message}. Run /pr-review to respond."

    # Sanitize strings for shell safety
    local safe_title safe_message safe_pr_title
    safe_title=$(sanitize_for_applescript "$title")
    safe_message=$(sanitize_for_applescript "$message")
    safe_pr_title=$(sanitize_for_applescript "$pr_title")

    # Use osascript for macOS notification
    osascript -e "display notification \"$safe_message\" with title \"$safe_title\" sound name \"$sound\"" 2>/dev/null || true

    # Also use terminal-notifier if available
    if command -v terminal-notifier &> /dev/null; then
        terminal-notifier \
            -title "$safe_title" \
            -subtitle "$safe_pr_title" \
            -message "$safe_message" \
            -sound "$sound" \
            -group "pr-review-$pr_number" \
            -activate "com.apple.Terminal" 2>/dev/null || true
    fi

    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} Notified: PR #$pr_number - $review_state by @$reviewer"

    # Auto-respond if enabled
    if [[ "$AUTO_RESPOND" == "true" ]]; then
        spawn_claude_pr_review "$pr_number" "$pr_title" "$reviewer" "$review_state"
    fi
}

# Get state for a PR
get_pr_state() {
    local pr_number="$1"
    jq -r ".\"$pr_number\" // \"{}\"" "$STATE_FILE"
}

# Update state for a PR
update_pr_state() {
    local pr_number="$1"
    local last_review_id="$2"
    local last_comment_count="$3"
    local review_decision="$4"
    local copilot_pending="${5:-0}"

    local tmp_file=$(mktemp)
    jq --arg pr "$pr_number" \
       --arg rid "$last_review_id" \
       --arg cc "$last_comment_count" \
       --arg rd "$review_decision" \
       --arg cp "$copilot_pending" \
       '.[$pr] = {"last_review_id": $rid, "comment_count": $cc, "review_decision": $rd, "copilot_pending": $cp, "checked_at": now}' \
       "$STATE_FILE" > "$tmp_file" && mv "$tmp_file" "$STATE_FILE"
}

# Remove state for closed/merged PRs
cleanup_state() {
    local open_prs="$1"  # comma-separated list of open PR numbers

    local tmp_file=$(mktemp)
    jq --arg open "$open_prs" '
        ($open | split(",")) as $open_list |
        with_entries(select(.key | IN($open_list[])))
    ' "$STATE_FILE" > "$tmp_file" && mv "$tmp_file" "$STATE_FILE"
}

# Check if reviewer is Copilot
is_copilot_reviewer() {
    local reviewer="$1"
    [[ "$reviewer" == "$COPILOT_REVIEWER" ]]
}

# Check for pending Copilot review comments
# Returns the count of unresolved Copilot comments
# Uses cursor-based pagination to handle PRs with >100 review threads
check_copilot_pending_comments() {
    local pr_number="$1"
    local total_count=0
    local cursor=""
    local has_next_page="true"
    local owner="${REPO%%/*}"
    local repo="${REPO##*/}"

    local result=""

    # Paginate through all review threads
    while true; do
        # Safety checks to prevent infinite pagination loops
        if [[ "$has_next_page" != "true" ]]; then
            break
        fi

        # If the API reports hasNextPage=true but gives a null/empty cursor
        # after at least one request, stop to avoid re-fetching the first page.
        if [[ -n "$result" && ( -z "$cursor" || "$cursor" == "null" ) ]]; then
            break
        fi

        local cursor_arg=""

        # Add cursor argument if we have one (not first page)
        if [[ -n "$cursor" && "$cursor" != "null" ]]; then
            cursor_arg="-f cursor=$cursor"
        fi

        # Query review threads with pagination
        # shellcheck disable=SC2086
        result=$(gh api graphql -f query='
            query($owner: String!, $repo: String!, $pr: Int!, $cursor: String) {
                repository(owner: $owner, name: $repo) {
                    pullRequest(number: $pr) {
                        reviewThreads(first: 100, after: $cursor) {
                            pageInfo {
                                hasNextPage
                                endCursor
                            }
                            nodes {
                                isResolved
                                comments(first: 1) {
                                    nodes {
                                        author {
                                            login
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        ' -f owner="$owner" -f repo="$repo" -F pr="$pr_number" $cursor_arg 2>/dev/null) || {
            # On error, return current count
            echo "$total_count"
            return
        }

        # Extract page count of unresolved Copilot comments
        local page_count
        page_count=$(echo "$result" | jq '[.data.repository.pullRequest.reviewThreads.nodes[] |
              select(.isResolved == false) |
              select(.comments.nodes[0]?.author?.login == "'"$COPILOT_REVIEWER"'")] | length' 2>/dev/null) || page_count=0

        # Accumulate total
        total_count=$((total_count + page_count))

        # Get pagination info for next iteration's safety checks
        has_next_page=$(echo "$result" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage // "false"' 2>/dev/null) || has_next_page="false"
        cursor=$(echo "$result" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor // "null"' 2>/dev/null) || cursor="null"
    done

    echo "$total_count"
}

# Check PRs for new reviews
check_prs() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} Checking PRs for $REPO..."

    # Get user's open PRs
    local prs
    prs=$(gh api "repos/$REPO/pulls?state=open" \
        --jq '.[] | select(.user.login == env.USER or .user.login == "'$(gh api user -q .login)'") | {number, title, reviewDecision: .reviewDecision}' 2>/dev/null) || true

    if [[ -z "$prs" ]]; then
        # Try alternative approach
        prs=$(gh pr list --repo "$REPO" --author "@me" --state open --json number,title 2>/dev/null) || true
    fi

    if [[ -z "$prs" || "$prs" == "[]" ]]; then
        echo -e "${YELLOW}[$(date '+%H:%M:%S')]${NC} No open PRs found"
        return 0
    fi

    # Get list of open PR numbers for cleanup
    local open_pr_numbers
    open_pr_numbers=$(echo "$prs" | jq -r 'if type == "array" then .[].number else .number end' | tr '\n' ',' | sed 's/,$//')

    # Normalize prs to newline-separated JSON objects
    local prs_normalized
    prs_normalized=$(echo "$prs" | jq -c 'if type == "array" then .[] else . end')

    # Process each PR (use process substitution to avoid subshell)
    while read -r pr; do
        [[ -z "$pr" ]] && continue

        local pr_number pr_title
        pr_number=$(echo "$pr" | jq -r '.number')
        pr_title=$(echo "$pr" | jq -r '.title')

        # Get reviews for this PR
        local reviews
        reviews=$(gh api "repos/$REPO/pulls/$pr_number/reviews" --jq '
            [.[] | {id, user: .user.login, state, submitted_at}] | sort_by(.submitted_at) | last
        ' 2>/dev/null) || true

        if [[ -z "$reviews" || "$reviews" == "null" ]]; then
            continue
        fi

        local latest_review_id latest_reviewer latest_state
        latest_review_id=$(echo "$reviews" | jq -r '.id // ""')
        latest_reviewer=$(echo "$reviews" | jq -r '.user // ""')
        latest_state=$(echo "$reviews" | jq -r '.state // ""')

        # Check if this is a Copilot review
        local is_copilot=false
        if is_copilot_reviewer "$latest_reviewer"; then
            is_copilot=true
            if [[ "$INCLUDE_COPILOT" != "true" ]]; then
                echo -e "${YELLOW}[$(date '+%H:%M:%S')]${NC} Skipping Copilot review for PR #$pr_number (--no-copilot)"
                # Update state to avoid repeated processing of the same Copilot review
                if [[ ! -f "$STATE_FILE" ]]; then
                    echo '{}' >"$STATE_FILE"
                fi
                local tmp_state_file
                tmp_state_file="$(mktemp)"
                jq --arg pr "$pr_number" \
                   --arg rid "$latest_review_id" \
                   --arg cp "0" \
                   '
                   .[$pr] = (.[$pr] // {}) |
                   .[$pr].last_review_id = $rid |
                   .[$pr].copilot_pending = $cp
                   ' "$STATE_FILE" >"$tmp_state_file"
                mv "$tmp_state_file" "$STATE_FILE"
                continue
            fi
        fi

        # Get current state
        local current_state
        current_state=$(get_pr_state "$pr_number")
        local stored_review_id stored_copilot_pending
        stored_review_id=$(echo "$current_state" | jq -r '.last_review_id // ""')
        stored_copilot_pending=$(echo "$current_state" | jq -r '.copilot_pending // "0"')

        # Check Copilot pending comments (only when Copilot review is detected)
        local copilot_pending="0"
        if [[ "$INCLUDE_COPILOT" == "true" && "$is_copilot" == "true" ]]; then
            copilot_pending=$(check_copilot_pending_comments "$pr_number")
        fi

        # Determine if we should notify
        local should_notify=false

        # Check if there's a new review
        if [[ -n "$latest_review_id" && "$latest_review_id" != "$stored_review_id" ]]; then
            should_notify=true
        fi

        # Check if there are new Copilot pending comments (even if review ID is same)
        if [[ "$is_copilot" == "true" && "$copilot_pending" -gt 0 && "$copilot_pending" != "$stored_copilot_pending" ]]; then
            should_notify=true
            echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} Copilot has $copilot_pending pending comments on PR #$pr_number"
        fi

        if [[ "$should_notify" == "true" ]]; then
            send_notification "$pr_number" "$pr_title" "$latest_reviewer" "$latest_state"

            # Get comment count
            local comment_count
            comment_count=$(gh api "repos/$REPO/pulls/$pr_number/comments" --jq 'length' 2>/dev/null) || comment_count="0"

            # Get review decision
            local review_decision
            review_decision=$(gh api "repos/$REPO/pulls/$pr_number" --jq '.reviewDecision // ""' 2>/dev/null) || review_decision=""

            update_pr_state "$pr_number" "$latest_review_id" "$comment_count" "$review_decision" "$copilot_pending"
        fi
    done < <(echo "$prs_normalized")

    # Cleanup state for closed PRs
    if [[ -n "$open_pr_numbers" ]]; then
        cleanup_state "$open_pr_numbers"
    fi

    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} Check complete"
}

# Main loop
main() {
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║           PR Review Polling Daemon                         ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "📦 Repository: ${GREEN}$REPO${NC}"
    echo -e "⏱️  Interval: ${GREEN}${POLL_INTERVAL}s${NC}"
    echo -e "📁 State file: ${GREEN}$STATE_FILE${NC}"
    if [[ "$AUTO_RESPOND" == "true" ]]; then
        echo -e "🤖 Auto-respond: ${GREEN}ENABLED${NC}"
        echo -e "📂 Working dir: ${GREEN}$WORKING_DIR${NC}"
    else
        echo -e "🤖 Auto-respond: ${YELLOW}DISABLED${NC}"
    fi
    if [[ "$INCLUDE_COPILOT" == "true" ]]; then
        echo -e "🤖 Copilot reviews: ${GREEN}INCLUDED${NC}"
    else
        echo -e "🤖 Copilot reviews: ${YELLOW}EXCLUDED${NC}"
    fi
    echo ""

    if [[ "$RUN_ONCE" == "true" ]]; then
        echo -e "${YELLOW}Running once...${NC}"
        check_prs
        exit 0
    fi

    echo -e "${GREEN}Starting daemon... (Ctrl+C to stop)${NC}"
    echo ""

    while true; do
        check_prs
        echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} Next check in ${POLL_INTERVAL}s"
        sleep "$POLL_INTERVAL"
    done
}

# Run main
main

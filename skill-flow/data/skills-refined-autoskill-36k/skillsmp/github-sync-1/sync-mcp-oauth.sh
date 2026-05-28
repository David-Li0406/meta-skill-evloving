#!/usr/bin/env bash
#
# sync-mcp-oauth.sh - Sync MCP OAuth credentials across Macs via iCloud
#
# Part of the github-sync skill for Claude Code.
# Automatically syncs .credentials.json at session start/end.
#
# Usage:
#   sync-mcp-oauth.sh push [--quiet]    - Push credentials to iCloud
#   sync-mcp-oauth.sh pull [--quiet]    - Pull credentials from iCloud
#   sync-mcp-oauth.sh status            - Show sync status
#

set -e

# Constants
CREDENTIALS_FILE="$HOME/.claude/.credentials.json"
ICLOUD_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs"
ICLOUD_SYNC_DIR="$ICLOUD_DIR/.deep-env"
ENCRYPTED_FILE="$ICLOUD_SYNC_DIR/mcp-oauth.enc"
CONFIG_DIR="$HOME/.config/deep-env"
STORED_PASS_FILE="$CONFIG_DIR/.sync_pass"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Quiet mode flag
QUIET=false

# ============================================================================
# Utility Functions
# ============================================================================

print_header() {
    [ "$QUIET" = true ] && return
    echo -e "${BOLD}${BLUE}$1${NC}"
}

print_success() {
    [ "$QUIET" = true ] && return
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

print_warning() {
    [ "$QUIET" = true ] && return
    echo -e "${YELLOW}!${NC} $1"
}

print_info() {
    [ "$QUIET" = true ] && return
    echo -e "${CYAN}→${NC} $1"
}

# ============================================================================
# Merge Functions
# ============================================================================

# Merge two .credentials.json files, keeping fresher tokens
merge_credentials() {
    local local_file="$1"
    local remote_file="$2"
    local output_file="$3"

    # Check if jq is available
    if ! command -v jq &> /dev/null; then
        print_warning "jq not found - using simple merge (remote overwrites local)"
        cp "$remote_file" "$output_file"
        return
    fi

    # Merge logic: For each OAuth entry, keep the one with later expiresAt
    jq -s '
        def merge_oauth(local; remote):
            if local.expiresAt == null and remote.expiresAt == null then
                remote
            elif local.expiresAt == null then
                remote
            elif remote.expiresAt == null then
                local
            elif (remote.expiresAt > local.expiresAt) then
                remote
            else
                local
            end;

        .[0] as $local | .[1] as $remote |
        {
            claudeAiOauth: merge_oauth($local.claudeAiOauth; $remote.claudeAiOauth),
            mcpOAuth: (
                # Merge mcpOAuth by server key
                ($local.mcpOAuth // {}) as $localMcp |
                ($remote.mcpOAuth // {}) as $remoteMcp |
                ($localMcp + $remoteMcp | to_entries | reduce .[] as $entry (
                    {};
                    . + {
                        ($entry.key): merge_oauth(
                            $localMcp[$entry.key] // {};
                            $remoteMcp[$entry.key] // {}
                        )
                    }
                ))
            )
        }
    ' "$local_file" "$remote_file" > "$output_file"
}

# ============================================================================
# Commands
# ============================================================================

cmd_push() {
    print_header "Pushing MCP OAuth credentials to iCloud"
    [ "$QUIET" = false ] && echo ""

    # Check if credentials file exists
    if [ ! -f "$CREDENTIALS_FILE" ]; then
        print_error "No credentials file found at $CREDENTIALS_FILE"
        exit 1
    fi

    # Check if iCloud Drive exists
    if [ ! -d "$ICLOUD_DIR" ]; then
        print_error "iCloud Drive not found at $ICLOUD_DIR"
        print_info "Make sure iCloud Drive is enabled in System Settings"
        exit 1
    fi

    # Create sync directory
    mkdir -p "$ICLOUD_SYNC_DIR"

    # Get password
    local password=""
    if [ -n "$DEEP_ENV_PASSWORD" ]; then
        password="$DEEP_ENV_PASSWORD"
    elif [ -f "$STORED_PASS_FILE" ]; then
        password=$(cat "$STORED_PASS_FILE")
    else
        print_error "No sync password found"
        print_info "Run 'deep-env push' first to set up the sync password"
        exit 1
    fi

    # Encrypt and save
    if openssl enc -aes-256-cbc -salt -pbkdf2 -in "$CREDENTIALS_FILE" -out "$ENCRYPTED_FILE" -pass pass:"$password" 2>/dev/null; then
        chmod 600 "$ENCRYPTED_FILE"
        print_success "Pushed MCP OAuth credentials to iCloud"
        [ "$QUIET" = false ] && print_info "Location: $ENCRYPTED_FILE"
    else
        print_error "Encryption failed"
        exit 1
    fi
}

cmd_pull() {
    print_header "Pulling MCP OAuth credentials from iCloud"
    [ "$QUIET" = false ] && echo ""

    # Check if encrypted file exists
    if [ ! -f "$ENCRYPTED_FILE" ]; then
        [ "$QUIET" = false ] && print_info "No synced credentials found in iCloud"
        [ "$QUIET" = false ] && print_info "Run 'sync-mcp-oauth.sh push' on another Mac first"
        exit 0
    fi

    # Get password
    local password=""
    if [ -n "$DEEP_ENV_PASSWORD" ]; then
        password="$DEEP_ENV_PASSWORD"
    elif [ -f "$STORED_PASS_FILE" ]; then
        password=$(cat "$STORED_PASS_FILE")
    else
        print_error "No sync password found"
        print_info "Run 'deep-env push' first to set up the sync password"
        exit 1
    fi

    # Decrypt to temp file
    local temp_file=$(mktemp)
    if ! openssl enc -aes-256-cbc -d -salt -pbkdf2 -in "$ENCRYPTED_FILE" -out "$temp_file" -pass pass:"$password" 2>/dev/null; then
        rm "$temp_file" 2>/dev/null || true
        print_error "Decryption failed - wrong password?"
        exit 1
    fi

    # If local file exists, merge; otherwise just copy
    if [ -f "$CREDENTIALS_FILE" ]; then
        local merged_file=$(mktemp)
        merge_credentials "$CREDENTIALS_FILE" "$temp_file" "$merged_file"
        mv "$merged_file" "$CREDENTIALS_FILE"
        chmod 600 "$CREDENTIALS_FILE"
        print_success "Merged remote credentials with local"
    else
        mv "$temp_file" "$CREDENTIALS_FILE"
        chmod 600 "$CREDENTIALS_FILE"
        print_success "Pulled MCP OAuth credentials from iCloud"
    fi

    rm -f "$temp_file"
}

cmd_status() {
    print_header "MCP OAuth Sync Status"
    echo ""

    # Check local file
    if [ -f "$CREDENTIALS_FILE" ]; then
        print_success "Local credentials: $CREDENTIALS_FILE"
        if command -v jq &> /dev/null; then
            local mcp_count=$(jq '.mcpOAuth | length' "$CREDENTIALS_FILE" 2>/dev/null || echo "?")
            print_info "MCP OAuth entries: $mcp_count"
        fi
    else
        print_warning "No local credentials file"
    fi

    echo ""

    # Check iCloud file
    if [ -f "$ENCRYPTED_FILE" ]; then
        print_success "iCloud backup: $ENCRYPTED_FILE"
        local size=$(ls -lh "$ENCRYPTED_FILE" | awk '{print $5}')
        local mod_time=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$ENCRYPTED_FILE" 2>/dev/null || stat -c "%y" "$ENCRYPTED_FILE" 2>/dev/null | cut -d'.' -f1)
        print_info "Size: $size, Modified: $mod_time"
    else
        print_warning "No iCloud backup found"
        print_info "Run 'sync-mcp-oauth.sh push' to create a backup"
    fi

    echo ""

    # Check password
    if [ -f "$STORED_PASS_FILE" ]; then
        print_success "Sync password is configured"
    else
        print_warning "No sync password found"
        print_info "Run 'deep-env push' to set up the sync password"
    fi
}

cmd_help() {
    cat << 'EOF'
sync-mcp-oauth.sh - Sync MCP OAuth credentials across Macs

USAGE:
    sync-mcp-oauth.sh <command> [options]

COMMANDS:
    push [--quiet]    Push credentials to iCloud
    pull [--quiet]    Pull credentials from iCloud (merges with local)
    status            Show sync status
    help              Show this help message

EXAMPLES:
    # After authenticating MCP servers, push to iCloud:
    sync-mcp-oauth.sh push

    # On another Mac, pull from iCloud:
    sync-mcp-oauth.sh pull

    # Check sync status:
    sync-mcp-oauth.sh status

NOTES:
    - Uses the same encryption password as deep-env
    - Credentials are merged: fresher tokens (later expiresAt) are kept
    - Runs automatically at session start (pull) and end (push)
    - Encrypted file stored at: ~/Library/Mobile Documents/com~apple~CloudDocs/.deep-env/mcp-oauth.enc

EOF
}

# ============================================================================
# Main
# ============================================================================

main() {
    local command="${1:-help}"
    shift || true

    # Parse global flags
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --quiet|-q)
                QUIET=true
                shift
                ;;
            *)
                break
                ;;
        esac
    done

    case "$command" in
        push)
            cmd_push
            ;;
        pull)
            cmd_pull
            ;;
        status)
            cmd_status
            ;;
        help|--help|-h)
            cmd_help
            ;;
        *)
            print_error "Unknown command: $command"
            echo "Run 'sync-mcp-oauth.sh help' for usage"
            exit 1
            ;;
    esac
}

main "$@"

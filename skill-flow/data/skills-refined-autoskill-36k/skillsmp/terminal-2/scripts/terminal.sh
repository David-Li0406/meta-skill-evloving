#!/usr/bin/env bash
# Terminal session management using tmux
# Provides interactive terminal sessions for TTY-requiring commands

set -euo pipefail

SOCKET_DIR="${TMPDIR:-/tmp}/ai-tmux-sockets"
SOCKET_PATH="$SOCKET_DIR/ai-tmux.sock"
LAST_SESSION_FILE="$SOCKET_DIR/.last_session"
TMUX_CONF="$SOCKET_DIR/tmux.conf"

# Common tmux options (use empty config to ignore user settings)
TMUX_OPTS=(-S "$SOCKET_PATH" -f "$TMUX_CONF")

# Initialize socket directory and config
init_socket_dir() {
    if [[ ! -d "$SOCKET_DIR" ]]; then
        mkdir -p "$SOCKET_DIR"
    fi
    # Create minimal tmux config (ignores user's ~/.tmux.conf)
    if [[ ! -f "$TMUX_CONF" ]]; then
        cat > "$TMUX_CONF" << 'EOF'
# Minimal tmux config for AI terminal sessions
set -g default-shell "/bin/bash"
set -g default-command "env -i HOME=\"$HOME\" PATH=\"$PATH\" TERM=\"$TERM\" bash --norc --noprofile"
EOF
    fi
}

# Generate a unique session name
generate_session_name() {
    echo "ai-terminal-$(head -c 4 /dev/urandom | xxd -p)"
}

# Check if session exists
session_exists() {
    local session_name="$1"
    tmux "${TMUX_OPTS[@]}" has-session -t "$session_name" 2>/dev/null
}

# Create a new tmux session
create_session() {
    local session_name="$1"
    local width="${2:-}"
    local height="${3:-}"
    
    local args=("${TMUX_OPTS[@]}" new-session -d -s "$session_name")
    
    if [[ -n "$width" && -n "$height" ]]; then
        args+=(-x "$width" -y "$height")
    fi
    
    tmux "${args[@]}"
    sleep 0.1
}

# Get or create session
get_or_create_session() {
    local session_name="${1:-}"
    local width="${2:-}"
    local height="${3:-}"
    
    init_socket_dir
    
    if [[ -z "$session_name" ]]; then
        if [[ -f "$LAST_SESSION_FILE" ]]; then
            session_name=$(cat "$LAST_SESSION_FILE")
        else
            session_name=$(generate_session_name)
        fi
    fi
    
    if ! session_exists "$session_name"; then
        create_session "$session_name" "$width" "$height"
    fi
    
    echo "$session_name" > "$LAST_SESSION_FILE"
    echo "$session_name"
}

# Capture pane output
capture_output() {
    local session_name="$1"
    local raw_output="${2:-false}"
    
    if [[ "$raw_output" == "true" ]]; then
        # -e option preserves escape sequences
        tmux "${TMUX_OPTS[@]}" capture-pane -p -e -t "$session_name"
    else
        tmux "${TMUX_OPTS[@]}" capture-pane -p -t "$session_name"
    fi
}

# Close session
close_session() {
    local session_name="$1"
    tmux "${TMUX_OPTS[@]}" kill-session -t "$session_name" 2>/dev/null || true
    
    if [[ -f "$LAST_SESSION_FILE" ]]; then
        local last_session
        last_session=$(cat "$LAST_SESSION_FILE")
        if [[ "$last_session" == "$session_name" ]]; then
            rm -f "$LAST_SESSION_FILE"
        fi
    fi
}

# Cleanup all sessions
cleanup() {
    tmux "${TMUX_OPTS[@]}" kill-server 2>/dev/null || true
    rm -rf "$SOCKET_DIR"
}

# Main command dispatcher
main() {
    local cmd="${1:-}"
    shift || true
    
    case "$cmd" in
        execute)
            local session_name=""
            local read_wait=1000
            local key_delay=0
            local literal=false
            local raw_output=false
            local width=""
            local height=""
            local -a keys=()
            
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --session) session_name="$2"; shift 2 ;;
                    --read-wait) read_wait="$2"; shift 2 ;;
                    --key-delay) key_delay="$2"; shift 2 ;;
                    --literal) literal=true; shift ;;
                    --raw-output) raw_output=true; shift ;;
                    --width) width="$2"; shift 2 ;;
                    --height) height="$2"; shift 2 ;;
                    --) shift; keys+=("$@"); break ;;
                    *) keys+=("$1"); shift ;;
                esac
            done
            
            session_name=$(get_or_create_session "$session_name" "$width" "$height")
            
            if [[ ${#keys[@]} -gt 0 ]]; then
                if [[ "$literal" == "true" ]]; then
                    # Send all keys literally as one string
                    local all_keys="${keys[*]}"
                    tmux "${TMUX_OPTS[@]}" send-keys -l -t "$session_name" -- "$all_keys"
                elif [[ "$key_delay" -gt 0 ]]; then
                    # Send each key with delay
                    for key in "${keys[@]}"; do
                        tmux "${TMUX_OPTS[@]}" send-keys -t "$session_name" -- "$key"
                        sleep "$(echo "scale=3; $key_delay/1000" | bc)"
                    done
                else
                    # Send all keys at once
                    tmux "${TMUX_OPTS[@]}" send-keys -t "$session_name" -- "${keys[@]}"
                fi
                # Wait for output
                sleep "$(echo "scale=3; $read_wait/1000" | bc)"
            fi
            
            local output
            output=$(capture_output "$session_name" "$raw_output")
            
            echo "Session: $session_name"
            echo "---"
            echo "$output"
            ;;
        
        close)
            local session_name=""
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --session) session_name="$2"; shift 2 ;;
                    *) shift ;;
                esac
            done
            
            if [[ -z "$session_name" ]]; then
                echo "Error: --session is required" >&2
                exit 1
            fi
            
            close_session "$session_name"
            echo "Session $session_name closed"
            ;;
        
        cleanup)
            cleanup
            echo "All sessions cleaned up"
            ;;
        
        *)
            echo "Usage: $0 {execute|close|cleanup} [options] [keys...]"
            echo ""
            echo "Commands:"
            echo "  execute   Send keys and capture output"
            echo "    --session NAME    Session name (optional, auto-generated if omitted)"
            echo "    --read-wait MS    Wait time before capturing (default: 1000)"
            echo "    --key-delay MS    Delay between keys (default: 0)"
            echo "    --literal         Send keys literally without parsing special keys"
            echo "    --raw-output      Preserve escape sequences in output (for colored text)"
            echo "    --width N         Terminal width for new sessions"
            echo "    --height N        Terminal height for new sessions"
            echo "    [keys...]         Keys to send (special keys: Enter, Escape, Up, Down, etc.)"
            echo ""
            echo "  close     Close a session"
            echo "    --session NAME    Session name to close (required)"
            echo ""
            echo "  cleanup   Close all sessions and clean up"
            echo ""
            echo "Examples:"
            echo "  $0 execute 'echo hello' Enter"
            echo "  $0 execute --session my-session 'ls -la' Enter"
            echo "  $0 execute --literal 'text with Enter in it'"
            echo "  $0 close --session my-session"
            exit 1
            ;;
    esac
}

main "$@"

#!/bin/bash
# Build and run codex command with proper flags

set -e

# Defaults
MODEL=""
SANDBOX="read-only"
FULL_AUTO=""
WORKDIR=""
PROMPT=""
PROMPT_FILE=""
RESUME=""
OUTPUT_FILE=""

usage() {
    echo "Usage: $0 [options] <prompt>"
    echo ""
    echo "Options:"
    echo "  -m, --model MODEL      Model to use (uses codex default if not specified)"
    echo "  -s, --sandbox MODE     Sandbox: read-only|workspace-write|danger-full-access"
    echo "  -a, --auto             Enable full-auto mode (sandboxed auto-approve)"
    echo "  -d, --dir DIR          Working directory"
    echo "  -f, --file FILE        Read prompt from file"
    echo "  -o, --output FILE      Write last message to file"
    echo "  -r, --resume           Resume last session"
    echo "  -h, --help             Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 'Analyze the codebase structure'"
    echo "  $0 -a 'Review code for issues'"
    echo "  $0 -s workspace-write -a 'Fix the bug in auth.ts'"
    echo "  $0 -r 'Continue with the changes'"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -s|--sandbox)
            SANDBOX="$2"
            shift 2
            ;;
        -a|--auto)
            FULL_AUTO="--full-auto"
            shift
            ;;
        -d|--dir)
            WORKDIR="$2"
            shift 2
            ;;
        -f|--file)
            PROMPT_FILE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -r|--resume)
            RESUME="true"
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            PROMPT="$1"
            shift
            ;;
    esac
done

# Read prompt from file if specified
if [ -n "$PROMPT_FILE" ]; then
    if [ ! -f "$PROMPT_FILE" ]; then
        echo "ERROR: Prompt file not found: $PROMPT_FILE"
        exit 1
    fi
    PROMPT=$(cat "$PROMPT_FILE")
fi

if [ -z "$PROMPT" ]; then
    echo "ERROR: Prompt required (use -f FILE or provide as argument)"
    usage
    exit 1
fi

# Build command
if [ "$RESUME" = "true" ]; then
    # Resume mode
    codex exec --skip-git-repo-check resume --last <<< "$PROMPT"
else
    # New session
    CMD=(codex exec --skip-git-repo-check)
    [ -n "$MODEL" ] && CMD+=(-m "$MODEL")
    CMD+=(--sandbox "$SANDBOX")

    [ -n "$FULL_AUTO" ] && CMD+=($FULL_AUTO)
    [ -n "$WORKDIR" ] && CMD+=(-C "$WORKDIR")
    [ -n "$OUTPUT_FILE" ] && CMD+=(-o "$OUTPUT_FILE")

    CMD+=("$PROMPT")

    "${CMD[@]}"
fi

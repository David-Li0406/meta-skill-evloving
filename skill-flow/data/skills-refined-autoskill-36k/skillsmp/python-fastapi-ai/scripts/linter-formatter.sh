#!/bin/bash

set -e

CHECK_MODE=false
FIX_MODE=false
VERBOSE=false
TARGET_PATH="."

show_help() {
    echo "Usage: $(basename "$0") [OPTIONS] [PATH]"
    echo ""
    echo "Run Ruff linter and formatter for Python code"
    echo ""
    echo "Options:"
    echo "  -c, --check     Check only - don't modify files (exit 1 if issues found)"
    echo "  -f, --fix       Auto-fix all fixable issues"
    echo "  -v, --verbose   Show verbose output"
    echo "  -h, --help      Show this help message"
    echo ""
    echo "Arguments:"
    echo "  PATH            Target path to lint/format (default: current directory)"
    echo ""
    echo "Examples:"
    echo "  $(basename "$0")                    # Format all Python files"
    echo "  $(basename "$0") --check            # Check without modifying"
    echo "  $(basename "$0") --fix src/         # Fix issues in src/"
    echo "  $(basename "$0") -c app/main.py     # Check single file"
}

while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--check)
            CHECK_MODE=true
            shift
            ;;
        -f|--fix)
            FIX_MODE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            TARGET_PATH="$1"
            shift
            ;;
    esac
done

check_ruff() {
    if command -v ruff &> /dev/null; then
        return 0
    elif command -v uv &> /dev/null; then
        echo "Using uv to run ruff..."
        UV_MODE=true
        return 0
    elif [[ -f ".venv/bin/ruff" ]]; then
        VENV_RUFF=".venv/bin/ruff"
        return 0
    elif [[ -f "venv/bin/ruff" ]]; then
        VENV_RUFF="venv/bin/ruff"
        return 0
    else
        echo "Error: ruff not found"
        echo "Install with: pip install ruff"
        echo "Or with uv: uv tool install ruff"
        exit 1
    fi
}

run_ruff() {
    local cmd="$1"
    shift
    local args=("$@")

    if [[ -n "$UV_MODE" ]]; then
        uv run ruff "$cmd" "${args[@]}"
    elif [[ -n "$VENV_RUFF" ]]; then
        "$VENV_RUFF" "$cmd" "${args[@]}"
    else
        ruff "$cmd" "${args[@]}"
    fi
}

build_check_args() {
    local args=("$TARGET_PATH")

    if [[ "$VERBOSE" == "true" ]]; then
        args+=("--verbose")
    fi

    echo "${args[@]}"
}

build_format_args() {
    local args=("$TARGET_PATH")

    if [[ "$CHECK_MODE" == "true" ]]; then
        args+=("--check" "--diff")
    fi

    if [[ "$VERBOSE" == "true" ]]; then
        args+=("--verbose")
    fi

    echo "${args[@]}"
}

build_lint_args() {
    local args=("$TARGET_PATH")

    if [[ "$FIX_MODE" == "true" ]]; then
        args+=("--fix")
    fi

    if [[ "$VERBOSE" == "true" ]]; then
        args+=("--verbose")
    fi

    echo "${args[@]}"
}

main() {
    check_ruff

    echo "=== Running Ruff Formatter ==="
    local format_args
    read -ra format_args <<< "$(build_format_args)"
    run_ruff format "${format_args[@]}"

    echo ""
    echo "=== Running Ruff Linter ==="
    local lint_args
    read -ra lint_args <<< "$(build_lint_args)"
    run_ruff check "${lint_args[@]}"

    echo ""
    echo "Done!"
}

main

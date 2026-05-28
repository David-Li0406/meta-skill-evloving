#!/usr/bin/env bash
# shellcheck shell=bash
#
# jd-tree: Display Johnny Decimal structure using tree
#
# Usage:
#   jd-tree                 # Show areas + categories (depth 2)
#   jd-tree 20              # Show area 20-29 structure
#   jd-tree 21              # Show category 21 structure
#   jd-tree 21.10           # Show specific ID structure
#   jd-tree -L3             # Full structure to ID level
#   jd-tree --porcelain     # No colors (for scripts/agents)

set -euo pipefail

# --- Load shared library ---
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/jd-lib.sh"

# --- Defaults ---
DEPTH=2
TARGET=""

# --- Argument Parsing ---
show_usage() {
    cat >&2 <<EOF
Usage: jd-tree [options] [area|category|id]

Display the Johnny Decimal directory structure using tree.

Options:
  -L <depth>    Set tree depth (default: 2)
  --porcelain   No colors, machine-readable output

Arguments:
  (none)        Show entire JD structure
  20 or 20-     Show area 20-29
  21            Show category 21
  21.10         Show specific ID

Examples:
  jd-tree              # Areas and categories
  jd-tree -L3          # Full structure including IDs
  jd-tree 20 -L2       # Area 20-29 with categories and IDs
  jd-tree --porcelain  # For agents
EOF
}

# Parse all arguments
JD_REMAINING_ARGS=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --porcelain)
            JD_PORCELAIN="true"
            shift
            ;;
        -L)
            if [[ -z "${2:-}" ]]; then
                jd_error "-L requires a depth value"
                exit 1
            fi
            DEPTH="$2"
            shift 2
            ;;
        -L[0-9]*)
            # Handle -L2 style (no space)
            DEPTH="${1#-L}"
            shift
            ;;
        --help|-h)
            show_usage
            exit 0
            ;;
        -*)
            jd_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
        *)
            JD_REMAINING_ARGS+=("$1")
            shift
            ;;
    esac
done

# Initialize colors after parsing
jd_init_colors

# Validate JD_ROOT exists
jd_validate_root || exit 1

# Get target from remaining args
if [[ ${#JD_REMAINING_ARGS[@]} -gt 1 ]]; then
    jd_error "Too many arguments"
    show_usage
    exit 1
elif [[ ${#JD_REMAINING_ARGS[@]} -eq 1 ]]; then
    TARGET="${JD_REMAINING_ARGS[0]}"
fi

# --- Resolve target directory ---
resolve_target() {
    local query="$1"

    if [[ -z "$query" ]]; then
        # No target: use JD_ROOT
        echo "$JD_ROOT"
        return 0
    fi

    # Area query (e.g., "20-29", "20-", or "20" for area)
    if [[ "$query" =~ ^[0-9][0-9]-[0-9]*$ ]] || [[ "$query" =~ ^[0-9]0$ ]]; then
        local area_prefix="${query:0:2}"
        find_area_dir "$area_prefix"
        return $?
    fi

    # Category query (e.g., "21")
    if [[ "$query" =~ ^[0-9][0-9]$ ]]; then
        find_category_dir "$query"
        return $?
    fi

    # ID query (e.g., "21.10")
    if [[ "$query" =~ ^[0-9][0-9]\.[0-9]+$ ]]; then
        find_id_dir "$query"
        return $?
    fi

    jd_error "Invalid query format '${query}'"
    return 1
}

# --- Build tree command ---
build_tree_args() {
    local -a args=()

    # Directories only
    args+=("-d")

    # Depth
    args+=("-L" "$DEPTH")

    # Sorting: version sort keeps "21.10" before "21.2" numerically
    args+=("--sort=version")

    # Colors based on mode
    if [[ "$JD_PORCELAIN" == "true" ]]; then
        args+=("-n")  # No colors
        args+=("--noreport")  # No summary line
    elif [[ -t 1 ]]; then
        args+=("-C")  # Force colors
    fi

    printf '%s\n' "${args[@]}"
}

# --- Main ---
target_dir=$(resolve_target "$TARGET") || exit 1

# Build tree arguments
mapfile -t tree_args < <(build_tree_args)

# Run tree
tree "${tree_args[@]}" "$target_dir"

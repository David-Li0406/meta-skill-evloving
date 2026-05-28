#!/usr/bin/env bash
# shellcheck shell=bash
#
# jd-move: Move a file to a Johnny Decimal location
#
# Usage:
#   jd-move document.pdf 21.10
#   jd-move document.pdf 21.10 new_name.pdf
#   jd-move --force document.pdf 21.10   # Allow overwrite
#   jd-move document.pdf 21.10 --porcelain  # Output full path (for agents)

set -euo pipefail

# --- Load shared library ---
# Resolve symlink to find actual script location
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/jd-lib.sh"

# Parse common args (--porcelain)
jd_parse_common_args "$@"
set -- "${JD_REMAINING_ARGS[@]}"

# Validate JD_ROOT exists
jd_validate_root || exit 1

# --- Parse arguments ---

force=false
dry_run=false
args=()
for arg in "$@"; do
    case "$arg" in
        --force|-f)
            force=true
            ;;
        --dry-run|-n)
            dry_run=true
            ;;
        *)
            args+=("$arg")
            ;;
    esac
done
set -- "${args[@]}"

if [[ $# -lt 2 ]] || [[ $# -gt 3 ]]; then
    echo "Usage: jd-move [--force] [--dry-run] <source> <ID> [new_name]" >&2
    echo "  jd-move document.pdf 21.10              # Move file" >&2
    echo "  jd-move my_folder 21.10                 # Move directory" >&2
    echo "  jd-move document.pdf 21.10 renamed.pdf  # Rename during move" >&2
    echo "  jd-move --force document.pdf 21.10      # Allow overwrite" >&2
    echo "  jd-move --dry-run document.pdf 21.10    # Preview without moving" >&2
    exit 1
fi

source_path="$1"
target_id="$2"
new_name="${3:-$(basename "$source_path")}"

# --- Validate inputs ---

# Check source exists (file or directory)
if [[ ! -e "$source_path" ]]; then
    jd_error "Source not found: ${source_path}"
    exit 1
fi

# Validate ID format
if [[ ! "$target_id" =~ ^[0-9][0-9]\.[0-9]+$ ]]; then
    jd_error "Invalid ID format '${target_id}'. Expected XX.YY (e.g., 21.10)"
    exit 1
fi

# Validate filename (if jd-validate exists)
if [[ -x "${SCRIPT_DIR}/jd-validate.sh" ]]; then
    if ! "${SCRIPT_DIR}/jd-validate.sh" "$new_name" >/dev/null 2>&1; then
        jd_warn "Filename may not follow conventions"
        "${SCRIPT_DIR}/jd-validate.sh" "$new_name" >&2 || true
    fi
fi

# Find target directory
target_dir=$(find_id_dir "$target_id") || exit 1

# Construct target path
target_path="${target_dir}/${new_name}"

# Check for existing file
if [[ -e "$target_path" ]]; then
    if [[ "$force" == true ]]; then
        jd_warn "Overwriting existing file: ${new_name}"
    else
        jd_error "Target file already exists: ${target_path}"
        echo "Use --force to overwrite" >&2
        exit 1
    fi
fi

# --- Perform the move ---

# Dry-run: just show what would happen
if [[ "$dry_run" == true ]]; then
    if [[ "$JD_PORCELAIN" == "true" ]]; then
        echo "$target_path"
    else
        echo "Would move: $(basename "$source_path") -> ${target_id}"
        echo "  From: ${source_path}"
        echo "  To:   ${target_path}"
    fi
    exit 0
fi

mv "$source_path" "$target_path"

if [[ "$JD_PORCELAIN" == "true" ]]; then
    echo "$target_path"
else
    jd_success "Moved: $(basename "$source_path") -> ${target_id}"
fi

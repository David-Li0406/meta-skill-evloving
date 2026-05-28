#!/usr/bin/env bash
# shellcheck shell=bash
#
# jd-mkdir: Create a new Johnny Decimal subcategory folder
#
# Usage:
#   jd-mkdir 21 "Chase Bank"           # Auto-assigns next ID (e.g., 21.15)
#   jd-mkdir 21 "Chase Bank" --id 15   # Explicit ID: 21.15
#   jd-mkdir 21 "Name" --porcelain     # Output full path (for agents)

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
explicit_id=""
category=""
name=""
dry_run=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --id)
            explicit_id="$2"
            shift 2
            ;;
        --dry-run|-n)
            dry_run=true
            shift
            ;;
        *)
            if [[ -z "$category" ]]; then
                category="$1"
            elif [[ -z "$name" ]]; then
                name="$1"
            else
                jd_error "Unexpected argument '$1'"
                exit 1
            fi
            shift
            ;;
    esac
done

# --- Validate inputs ---
if [[ -z "$category" ]] || [[ -z "$name" ]]; then
    echo "Usage: jd-mkdir <category> <name> [--id N] [--dry-run]" >&2
    echo "  jd-mkdir 21 \"Chase Bank\"           # Auto-assigns next ID" >&2
    echo "  jd-mkdir 21 \"Chase Bank\" --id 15   # Explicit: 21.15" >&2
    echo "  jd-mkdir 21 \"Chase Bank\" --dry-run # Preview without creating" >&2
    exit 1
fi

# Validate category format (XX)
if [[ ! "$category" =~ ^[0-9][0-9]$ ]]; then
    jd_error "Invalid category format '${category}'. Expected XX (e.g., 21)"
    exit 1
fi

# Find the category directory (validates it exists)
category_dir=$(find_category_dir "$category") || exit 1

# Determine the ID
if [[ -n "$explicit_id" ]]; then
    # Validate explicit ID is a number
    if [[ ! "$explicit_id" =~ ^[0-9]+$ ]]; then
        jd_error "--id must be a number, got '${explicit_id}'"
        exit 1
    fi
    id="${category}.${explicit_id}"
else
    # Auto-assign next available ID
    id=$(next_available_id "$category") || exit 1
fi

# Construct the new folder path
new_folder="${category_dir}/${id} ${name}"

# Check if it already exists
if [[ -e "$new_folder" ]]; then
    jd_error "Folder already exists: ${new_folder}"
    exit 1
fi

# Dry-run: just show what would be created
if [[ "$dry_run" == true ]]; then
    if [[ "$JD_PORCELAIN" == "true" ]]; then
        echo "$new_folder"
    else
        echo "Would create: ${id} ${name}"
        echo "  Path: ${new_folder}"
    fi
    exit 0
fi

# Create the folder
mkdir -p "$new_folder"
chmod 700 "$new_folder"

if [[ "$JD_PORCELAIN" == "true" ]]; then
    echo "$new_folder"
else
    jd_success "Created: ${id} ${name}"
fi

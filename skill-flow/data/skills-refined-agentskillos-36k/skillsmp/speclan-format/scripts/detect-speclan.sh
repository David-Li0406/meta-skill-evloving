#!/bin/bash
# Detect SPECLAN directory in a project
# Usage: detect-speclan.sh [start_directory]
# Returns: Path to speclan directory or exits with error

set -e

START_DIR="${1:-.}"
START_DIR=$(cd "$START_DIR" && pwd)

# Common speclan directory names
SPECLAN_DIRS=("speclan" "specs/speclan" ".speclan")

# Characteristic subdirectories that indicate a speclan directory
SPECLAN_MARKERS=("goals" "features" "requirements")

find_speclan_dir() {
    local dir="$1"

    for speclan_name in "${SPECLAN_DIRS[@]}"; do
        local candidate="$dir/$speclan_name"
        if [[ -d "$candidate" ]]; then
            # Verify it's actually a speclan directory by checking for markers
            local marker_count=0
            for marker in "${SPECLAN_MARKERS[@]}"; do
                if [[ -d "$candidate/$marker" ]]; then
                    ((marker_count++))
                fi
            done

            # Need at least 2 markers to confirm
            if [[ $marker_count -ge 2 ]]; then
                echo "$candidate"
                return 0
            fi
        fi
    done

    return 1
}

# Search from start directory up to root
current_dir="$START_DIR"
while [[ "$current_dir" != "/" ]]; do
    if result=$(find_speclan_dir "$current_dir"); then
        echo "$result"
        exit 0
    fi
    current_dir=$(dirname "$current_dir")
done

# Not found
echo "No SPECLAN directory found" >&2
exit 1

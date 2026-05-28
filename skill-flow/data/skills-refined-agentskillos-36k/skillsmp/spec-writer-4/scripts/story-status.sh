#!/usr/bin/env bash
#
# Quick overview of story states from STATE.md
#
# Usage: story-status.sh [--discovery-path PATH]
#

set -euo pipefail

# Parse arguments
discovery_path=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --discovery-path)
            discovery_path="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Usage: $0 [--discovery-path PATH]" >&2
            exit 1
            ;;
    esac
done

# Find discovery directory
if [ -n "$discovery_path" ]; then
    discovery_dir="$discovery_path"
elif [ "$(basename "$(pwd)")" = "discovery" ]; then
    discovery_dir="$(pwd)"
else
    # Look for discovery/ in current or parent directories
    current="$(pwd)"
    discovery_dir=""
    while [ "$current" != "/" ]; do
        if [ -d "$current/discovery" ]; then
            discovery_dir="$current/discovery"
            break
        fi
        current="$(dirname "$current")"
    done

    if [ -z "$discovery_dir" ]; then
        echo "ERROR: discovery/ directory not found" >&2
        echo "HINT: Run from within discovery/, provide --discovery-path, or ensure discovery/ exists in a parent directory" >&2
        exit 1
    fi
fi

# Check if STATE.md exists
state_file="$discovery_dir/STATE.md"
if [ ! -f "$state_file" ]; then
    echo "ERROR: STATE.md not found in $discovery_dir" >&2
    exit 1
fi

# Extract and display story status overview
echo "Story Status Overview"
echo "====================="
echo ""

# Extract the Story Status Overview table
in_table=false
while IFS= read -r line; do
    if [[ "$line" =~ ^##[[:space:]]Story[[:space:]]Status[[:space:]]Overview ]]; then
        in_table=true
        continue
    fi

    if $in_table; then
        # Stop at next section header
        if [[ "$line" =~ ^## ]]; then
            break
        fi

        # Print table lines
        if [[ "$line" =~ ^\| ]]; then
            echo "$line"
        fi
    fi
done < "$state_file"

echo ""

# Count stories by status
echo "Summary:"
in_spec=$(grep -c "✅ In SPEC" "$state_file" || echo "0")
in_progress=$(grep -c "🔄 In Progress" "$state_file" || echo "0")
queued=$(grep -c "⏳ Queued" "$state_file" || echo "0")
new=$(grep -c "🆕 New" "$state_file" || echo "0")

echo "  ✅ In SPEC: $in_spec"
echo "  🔄 In Progress: $in_progress"
echo "  ⏳ Queued: $queued"
echo "  🆕 New: $new"
echo ""

total=$((in_spec + in_progress + queued + new))
if [ $total -gt 0 ]; then
    percent_complete=$((in_spec * 100 / total))
    echo "Progress: $percent_complete% ($in_spec/$total stories completed)"
fi

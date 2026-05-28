#!/usr/bin/env bash
#
# Initialize discovery/ directory structure for a new spec
#
# Usage: init-spec.sh <feature-name> [--base-path <path>]
#

set -euo pipefail

# Parse arguments
feature_name=""
base_path="."

while [ $# -gt 0 ]; do
    case "$1" in
        --base-path)
            if [ $# -lt 2 ]; then
                echo "ERROR: --base-path requires a value" >&2
                exit 1
            fi
            base_path="$2"
            shift 2
            ;;
        -*)
            echo "ERROR: Unknown option: $1" >&2
            echo "Usage: $0 <feature-name> [--base-path <path>]" >&2
            exit 1
            ;;
        *)
            if [ -z "$feature_name" ]; then
                feature_name="$1"
            else
                echo "ERROR: Too many positional arguments" >&2
                echo "Usage: $0 <feature-name> [--base-path <path>]" >&2
                exit 1
            fi
            shift
            ;;
    esac
done

# Check required arguments
if [ -z "$feature_name" ]; then
    echo "Usage: $0 <feature-name> [--base-path <path>]" >&2
    echo "" >&2
    echo "Example: $0 payment-flow-redesign --base-path /path/to/project" >&2
    exit 1
fi

# Resolve absolute base path
if [ ! -d "$base_path" ]; then
    echo "ERROR: Base path does not exist: $base_path" >&2
    echo "HINT: Create the base directory first or use an existing path" >&2
    exit 1
fi
base_path=$(cd "$base_path" && pwd)
discovery_dir="$base_path/discovery"

# Check if discovery/ already exists
if [ -d "$discovery_dir" ]; then
    echo "ERROR: discovery/ directory already exists" >&2
    echo "HINT: Remove or rename existing discovery/ directory first" >&2
    exit 1
fi

# Get script directory for template path
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
template_dir="$script_dir/../templates/discovery-structure"

# Verify templates exist
if [ ! -d "$template_dir" ]; then
    echo "ERROR: Template directory not found: $template_dir" >&2
    exit 1
fi

# Create directory structure
echo "Creating discovery/ structure for: $feature_name"
mkdir -p "$discovery_dir/archive"

# Copy templates
cp "$template_dir/SPEC.md.template" "$discovery_dir/SPEC.md"
cp "$template_dir/STATE.md.template" "$discovery_dir/STATE.md"
cp "$template_dir/OPEN_QUESTIONS.md.template" "$discovery_dir/OPEN_QUESTIONS.md"
cp "$template_dir/archive/DECISIONS.md.template" "$discovery_dir/archive/DECISIONS.md"
cp "$template_dir/archive/RESEARCH.md.template" "$discovery_dir/archive/RESEARCH.md"
cp "$template_dir/archive/ITERATIONS.md.template" "$discovery_dir/archive/ITERATIONS.md"
cp "$template_dir/archive/REVISIONS.md.template" "$discovery_dir/archive/REVISIONS.md"

# Get current date and timestamp
date=$(date +%Y-%m-%d)
timestamp=$(date -u +"%Y-%m-%d %H:%M UTC")
author=$(git config user.name 2>/dev/null || echo "$USER")

# Replace placeholders in all files
for file in "$discovery_dir"/*.md "$discovery_dir"/archive/*.md; do
    # Use sed for in-place replacement (portable across macOS and Linux)
    sed -i.bak \
        -e "s/{FEATURE_NAME}/$feature_name/g" \
        -e "s/{DATE}/$date/g" \
        -e "s/{TIMESTAMP}/$timestamp/g" \
        -e "s/{AUTHOR}/$author/g" \
        "$file"
    rm "$file.bak"
done

echo "✓ Created discovery/ structure for: $feature_name"
echo ""
echo "Files created:"
echo "  discovery/SPEC.md"
echo "  discovery/STATE.md"
echo "  discovery/OPEN_QUESTIONS.md"
echo "  discovery/archive/DECISIONS.md"
echo "  discovery/archive/RESEARCH.md"
echo "  discovery/archive/ITERATIONS.md"
echo "  discovery/archive/REVISIONS.md"
echo ""
echo "Next steps:"
echo "  1. cd discovery/"
echo "  2. Review STATE.md and begin problem exploration"
echo "  3. Add questions with: ../scripts/add-question.py --question '...' --category blocking"
echo "  4. Log decisions and research as you progress"
echo ""
echo "Happy discovery! 🚀"

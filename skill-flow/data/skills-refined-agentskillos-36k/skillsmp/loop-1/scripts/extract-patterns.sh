#!/usr/bin/env bash
# extract-patterns.sh - Extract patterns from top-scoring projects
# Usage: ./extract-patterns.sh
# Reads from ~/.loop/discovered-projects.json
# Outputs to ~/.loop/patterns/

set -euo pipefail

DISCOVERY_FILE="${1:-$HOME/.loop/discovered-projects.json}"
PATTERNS_DIR="${2:-$HOME/.loop/patterns}"
MIN_SCORE="${3:-50}"

# Ensure patterns dir exists
mkdir -p "$PATTERNS_DIR"

echo "🎯 Extracting patterns from projects (min score: $MIN_SCORE)..." >&2

# Get top projects
if [[ ! -f "$DISCOVERY_FILE" ]]; then
    echo "❌ Discovery file not found: $DISCOVERY_FILE" >&2
    echo "Run discover-projects.sh first" >&2
    exit 1
fi

# Extract top projects (using jq if available, grep fallback)
if command -v jq &>/dev/null; then
    top_projects=$(jq -r ".[] | select(.score >= $MIN_SCORE) | .path" "$DISCOVERY_FILE")
else
    # Fallback: simple grep parsing
    top_projects=$(grep '"path"' "$DISCOVERY_FILE" | sed 's/.*"path": "\(.*\)".*/\1/')
fi

if [[ -z "$top_projects" ]]; then
    echo "⚠️  No projects meet minimum score threshold" >&2
    echo "Lowering threshold to 30 and trying again..." >&2
    MIN_SCORE=30
    if command -v jq &>/dev/null; then
        top_projects=$(jq -r ".[] | select(.score >= $MIN_SCORE) | .path" "$DISCOVERY_FILE")
    else
        top_projects=$(grep '"path"' "$DISCOVERY_FILE" | sed 's/.*"path": "\(.*\)".*/\1/')
    fi
fi

project_count=$(echo "$top_projects" | wc -l | tr -d ' ')
echo "📁 Analyzing $project_count projects..." >&2

# Extract each pattern type
"$(dirname "$0")/extract-file-structure.sh" "$top_projects" > "$PATTERNS_DIR/file-structure.md"
"$(dirname "$0")/extract-test-patterns.sh" "$top_projects" > "$PATTERNS_DIR/test-patterns.md"
"$(dirname "$0")/extract-convex-schema.sh" "$top_projects" > "$PATTERNS_DIR/convex-schema.md"
"$(dirname "$0")/extract-commit-style.sh" "$top_projects" > "$PATTERNS_DIR/commit-style.md"
"$(dirname "$0")/extract-import-patterns.sh" "$top_projects" > "$PATTERNS_DIR/import-patterns.md"
"$(dirname "$0")/extract-lint-patterns.sh" "$top_projects" > "$PATTERNS_DIR/lint-patterns.md"

echo "✅ Pattern extraction complete!" >&2
echo "" >&2
echo "Patterns saved to:" >&2
ls -lh "$PATTERNS_DIR"/*.md >&2

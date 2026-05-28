#!/bin/bash
# Auto-Capture Script for Knowledge Management
# Automatically captures session insights when git changes exceed threshold
#
# Usage: ./auto-capture.sh [project-root] [--force]
# Options:
#   --force    Skip minimum files check

set -e

# Validate path to prevent path traversal attacks
validate_path() {
    local path="$1"

    # Reject paths containing .. (path traversal)
    if [[ "$path" == *".."* ]]; then
        echo "❌ Error: Path cannot contain '..'" >&2
        exit 1
    fi

    # Resolve to absolute path
    local resolved_path
    resolved_path=$(cd "$path" 2>/dev/null && pwd) || {
        echo "❌ Error: Invalid path '$path'" >&2
        exit 1
    }

    echo "$resolved_path"
}

RAW_PROJECT_ROOT="${1:-.}"
PROJECT_ROOT=$(validate_path "$RAW_PROJECT_ROOT")
FORCE_CAPTURE=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --force)
            FORCE_CAPTURE=true
            shift
            ;;
    esac
done

# Configuration
MIN_CHANGED_FILES=3
TZ='Asia/Bangkok'
export TZ

# Get current date/time in Bangkok timezone
YEAR_MONTH=$(date '+%Y-%m')
DAY=$(date '+%d')
TIME=$(date '+%H.%M')
TIMESTAMP=$(date '+%Y-%m-%d_%H%M%S')

# Output directory
OUTPUT_DIR="$PROJECT_ROOT/docs/auto-captured/$YEAR_MONTH/$DAY"
SESSION_ID=$(date '+%s' | tail -c 5)
OUTPUT_FILE="$OUTPUT_DIR/${TIME}_session-${SESSION_ID}.md"

# Check if in git repository
if ! git -C "$PROJECT_ROOT" rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Get git changes summary
CHANGED_FILES=$(git -C "$PROJECT_ROOT" diff --name-only HEAD 2>/dev/null | wc -l | tr -d ' ')
STAGED_FILES=$(git -C "$PROJECT_ROOT" diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')
TOTAL_CHANGES=$((CHANGED_FILES + STAGED_FILES))

# Also count untracked files
UNTRACKED_FILES=$(git -C "$PROJECT_ROOT" ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')
TOTAL_WITH_UNTRACKED=$((TOTAL_CHANGES + UNTRACKED_FILES))

echo "📊 Session Summary:"
echo "   Changed files: $CHANGED_FILES"
echo "   Staged files: $STAGED_FILES"
echo "   Untracked files: $UNTRACKED_FILES"
echo "   Total: $TOTAL_WITH_UNTRACKED"

# Check minimum threshold
if [ "$FORCE_CAPTURE" = false ] && [ "$TOTAL_WITH_UNTRACKED" -lt "$MIN_CHANGED_FILES" ]; then
    echo ""
    echo "⏭️  Skipped: Less than $MIN_CHANGED_FILES files changed"
    echo "   Use --force to capture anyway"
    exit 0
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Get changed files list
CHANGED_LIST=$(git -C "$PROJECT_ROOT" diff --name-only HEAD 2>/dev/null)
STAGED_LIST=$(git -C "$PROJECT_ROOT" diff --cached --name-only 2>/dev/null)
UNTRACKED_LIST=$(git -C "$PROJECT_ROOT" ls-files --others --exclude-standard 2>/dev/null)

# Combine and deduplicate
ALL_FILES=$(echo -e "${CHANGED_LIST}\n${STAGED_LIST}\n${UNTRACKED_LIST}" | sort -u | grep -v '^$')

# Determine file types
FILE_TYPES=$(echo "$ALL_FILES" | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -5)

# Get recent commit messages for context
RECENT_COMMITS=$(git -C "$PROJECT_ROOT" log --oneline -5 2>/dev/null || echo "No commits yet")

# Generate draft content
cat > "$OUTPUT_FILE" << EOF
---
type: auto-captured
status: draft
captured_at: $(date '+%Y-%m-%d %H:%M:%S %Z')
session_id: $SESSION_ID
files_changed: $TOTAL_WITH_UNTRACKED
---

# Session Capture: $TIMESTAMP

## Summary

> **TODO**: Review and add context about what was accomplished in this session.

## Changes Overview

| Metric | Count |
|--------|-------|
| Changed files | $CHANGED_FILES |
| Staged files | $STAGED_FILES |
| New files | $UNTRACKED_FILES |
| **Total** | **$TOTAL_WITH_UNTRACKED** |

## File Types Modified

\`\`\`
$FILE_TYPES
\`\`\`

## Files Changed

\`\`\`
$ALL_FILES
\`\`\`

## Recent Commits

\`\`\`
$RECENT_COMMITS
\`\`\`

## Key Insights

> **TODO**: Add key insights from this session

- [ ] Insight 1
- [ ] Insight 2

## Context: Before

- **Problem**:
- **Existing Behavior**:
- **Metrics**:

## Context: After

- **Solution**:
- **New Behavior**:
- **Metrics**:

## Future Improvements

- [ ]

---

*Auto-captured by Knowledge Management System*
*Review and edit this draft, then move to \`docs/retrospective/\` when complete*
EOF

echo ""
echo "✅ Auto-captured to: $OUTPUT_FILE"
echo ""
echo "📝 Next steps:"
echo "   1. Review and edit the draft"
echo "   2. Add context and insights"
echo "   3. Move to docs/retrospective/ when complete"

#!/bin/bash
# AI-Powered Capture Script for Knowledge Management
# Uses Claude API to analyze git diff and generate intelligent summaries
#
# Usage: ./ai-capture.sh [project-root] [--force]
# Requirements: ANTHROPIC_API_KEY environment variable

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
API_MODEL="${CLAUDE_MODEL:-claude-sonnet-4-20250514}"

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY not set"
    echo ""
    echo "Set your API key:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    echo "Or use basic auto-capture instead:"
    echo "  ./auto-capture.sh"
    exit 1
fi

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

# Get git changes
CHANGED_FILES=$(git -C "$PROJECT_ROOT" diff --name-only HEAD 2>/dev/null | wc -l | tr -d ' ')
STAGED_FILES=$(git -C "$PROJECT_ROOT" diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')
UNTRACKED_FILES=$(git -C "$PROJECT_ROOT" ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')
TOTAL_CHANGES=$((CHANGED_FILES + STAGED_FILES + UNTRACKED_FILES))

echo "📊 Session Summary:"
echo "   Changed files: $CHANGED_FILES"
echo "   Staged files: $STAGED_FILES"
echo "   Untracked files: $UNTRACKED_FILES"
echo "   Total: $TOTAL_CHANGES"

# Check minimum threshold
if [ "$FORCE_CAPTURE" = false ] && [ "$TOTAL_CHANGES" -lt "$MIN_CHANGED_FILES" ]; then
    echo ""
    echo "⏭️  Skipped: Less than $MIN_CHANGED_FILES files changed"
    echo "   Use --force to capture anyway"
    exit 0
fi

echo ""
echo "🤖 Analyzing changes with AI..."

# Get git diff (limited to avoid token overflow)
GIT_DIFF=$(git -C "$PROJECT_ROOT" diff HEAD --stat 2>/dev/null | head -50)
GIT_DIFF_CONTENT=$(git -C "$PROJECT_ROOT" diff HEAD 2>/dev/null | head -200)
RECENT_COMMITS=$(git -C "$PROJECT_ROOT" log --oneline -5 2>/dev/null || echo "No commits yet")
ALL_FILES=$(git -C "$PROJECT_ROOT" diff --name-only HEAD 2>/dev/null; git -C "$PROJECT_ROOT" diff --cached --name-only 2>/dev/null; git -C "$PROJECT_ROOT" ls-files --others --exclude-standard 2>/dev/null)
ALL_FILES=$(echo "$ALL_FILES" | sort -u | grep -v '^$')

# Prepare prompt for Claude
PROMPT="Analyze this git session and generate a structured summary in Thai/English mixed style.

## Git Diff Stats:
\`\`\`
$GIT_DIFF
\`\`\`

## Recent Commits:
\`\`\`
$RECENT_COMMITS
\`\`\`

## Changed Files:
\`\`\`
$ALL_FILES
\`\`\`

## Diff Content (truncated):
\`\`\`
$GIT_DIFF_CONTENT
\`\`\`

Generate a JSON response with:
1. \"type\": one of [feature, bugfix, refactor, decision, discovery, config, docs]
2. \"title\": brief title (max 50 chars)
3. \"summary\": 2-3 sentence summary of what was done
4. \"tags\": array of 3-5 relevant tags
5. \"key_changes\": array of 3-5 key changes made
6. \"insights\": array of 1-3 key insights/learnings
7. \"before_context\": what problem/situation existed before
8. \"after_context\": what solution/state exists after

Respond ONLY with valid JSON, no markdown code blocks."

# Call Claude API
RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
    -H "Content-Type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d "$(jq -n \
        --arg model "$API_MODEL" \
        --arg prompt "$PROMPT" \
        '{
            model: $model,
            max_tokens: 1024,
            messages: [{role: "user", content: $prompt}]
        }')")

# Check for errors
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.error.message')
    echo "❌ API Error: $ERROR_MSG"
    echo ""
    echo "Falling back to basic auto-capture..."
    exec "$(dirname "$0")/auto-capture.sh" "$PROJECT_ROOT" --force
fi

# Extract content from response
AI_CONTENT=$(echo "$RESPONSE" | jq -r '.content[0].text' 2>/dev/null)

# Parse JSON response
TYPE=$(echo "$AI_CONTENT" | jq -r '.type // "discovery"' 2>/dev/null || echo "discovery")
TITLE=$(echo "$AI_CONTENT" | jq -r '.title // "Session Capture"' 2>/dev/null || echo "Session Capture")
SUMMARY=$(echo "$AI_CONTENT" | jq -r '.summary // ""' 2>/dev/null || echo "")
TAGS=$(echo "$AI_CONTENT" | jq -r '.tags // [] | join(", ")' 2>/dev/null || echo "")
KEY_CHANGES=$(echo "$AI_CONTENT" | jq -r '.key_changes // [] | .[] | "- " + .' 2>/dev/null || echo "- No changes detected")
INSIGHTS=$(echo "$AI_CONTENT" | jq -r '.insights // [] | .[] | "- " + .' 2>/dev/null || echo "- No insights")
BEFORE=$(echo "$AI_CONTENT" | jq -r '.before_context // ""' 2>/dev/null || echo "")
AFTER=$(echo "$AI_CONTENT" | jq -r '.after_context // ""' 2>/dev/null || echo "")

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Generate enhanced capture file
cat > "$OUTPUT_FILE" << EOF
---
type: $TYPE
status: ai-generated
captured_at: $(date '+%Y-%m-%d %H:%M:%S %Z')
session_id: $SESSION_ID
files_changed: $TOTAL_CHANGES
tags: [$TAGS]
---

# $TITLE

## Summary

$SUMMARY

## Changes Overview

| Metric | Count |
|--------|-------|
| Changed files | $CHANGED_FILES |
| Staged files | $STAGED_FILES |
| New files | $UNTRACKED_FILES |
| **Total** | **$TOTAL_CHANGES** |

## Key Changes

$KEY_CHANGES

## Files Modified

\`\`\`
$ALL_FILES
\`\`\`

## Key Insights

$INSIGHTS

## Context: Before

$BEFORE

## Context: After

$AFTER

## Recent Commits

\`\`\`
$RECENT_COMMITS
\`\`\`

## Future Improvements

- [ ] Review and validate AI-generated content
- [ ] Add additional context if needed

---

*AI-captured by Knowledge Management System using $API_MODEL*
*Review and move to \`docs/retrospective/\` when complete*
EOF

echo ""
echo "✅ AI-captured to: $OUTPUT_FILE"
echo ""
echo "📋 Generated:"
echo "   Type: $TYPE"
echo "   Title: $TITLE"
echo "   Tags: $TAGS"
echo ""
echo "📝 Next steps:"
echo "   1. Review AI-generated content"
echo "   2. Edit and refine as needed"
echo "   3. Move to docs/retrospective/ when complete"

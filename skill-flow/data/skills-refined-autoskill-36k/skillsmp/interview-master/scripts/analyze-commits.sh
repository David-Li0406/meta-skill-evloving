#!/usr/bin/env bash

# analyze-commits.sh - Extract commit history and patterns for resume generation
# Usage: ./analyze-commits.sh <author> <repo-path> [start-date] [end-date]

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Display usage
usage() {
    cat <<EOF
Usage: $0 <author> <repo-path> [start-date] [end-date]

Analyze git commit history for a specific author to generate resume content.

Arguments:
  author      Author name or email to analyze (e.g., "John Doe" or "john@example.com")
  repo-path   Path to git repository
  start-date  Optional: Start date in YYYY-MM-DD format (default: first commit)
  end-date    Optional: End date in YYYY-MM-DD format (default: today)

Examples:
  $0 "Jane Doe" /path/to/repo
  $0 "jane@example.com" /path/to/repo 2023-01-01 2024-01-01

Output:
  JSON formatted commit analysis data
EOF
    exit 1
}

# Validate arguments
if [[ $# -lt 2 ]]; then
    echo -e "${RED}Error: Missing required arguments${NC}" >&2
    usage
fi

AUTHOR="$1"
REPO_PATH="$2"
START_DATE="${3:-}"
END_DATE="${4:-$(date +%Y-%m-%d)}"

# Validate repository
if [[ ! -d "$REPO_PATH/.git" ]]; then
    echo -e "${RED}Error: Not a git repository: $REPO_PATH${NC}" >&2
    exit 1
fi

echo -e "${GREEN}Analyzing commits for author: $AUTHOR${NC}" >&2
echo -e "${GREEN}Repository: $REPO_PATH${NC}" >&2

cd "$REPO_PATH" || exit 1

# Build git log command
GIT_CMD="git log --author=\"$AUTHOR\" --no-merges --pretty=format:'%H|%ai|%s' --numstat"

if [[ -n "$START_DATE" ]]; then
    GIT_CMD+=" --since=\"$START_DATE\""
fi

if [[ -n "$END_DATE" ]]; then
    GIT_CMD+=" --until=\"$END_DATE\""
fi

# Get first and last commit dates
FIRST_COMMIT=$(git log --author="$AUTHOR" --reverse --pretty=format:'%ai' --no-merges | head -1)
LAST_COMMIT=$(git log --author="$AUTHOR" --pretty=format:'%ai' --no-merges | head -1)

if [[ -z "$FIRST_COMMIT" ]]; then
    echo -e "${RED}Error: No commits found for author: $AUTHOR${NC}" >&2
    exit 1
fi

# Count total commits
TOTAL_COMMITS=$(git log --author="$AUTHOR" --no-merges --oneline ${START_DATE:+--since="$START_DATE"} ${END_DATE:+--until="$END_DATE"} | wc -l)

# Calculate lines added/deleted
LINES_STATS=$(git log --author="$AUTHOR" --no-merges --numstat --pretty=tformat: ${START_DATE:+--since="$START_DATE"} ${END_DATE:+--until="$END_DATE"} | \
    awk '{added+=$1; deleted+=$2} END {printf "%d %d %d", added, deleted, added-deleted}')
read -r LINES_ADDED LINES_DELETED NET_LINES <<< "$LINES_STATS"

# Count files modified
FILES_MODIFIED=$(git log --author="$AUTHOR" --no-merges --name-only --pretty=format: ${START_DATE:+--since="$START_DATE"} ${END_DATE:+--until="$END_DATE"} | \
    sort | uniq | grep -v '^$' | wc -l)

# Calculate duration in months
if [[ -n "$FIRST_COMMIT" && -n "$LAST_COMMIT" ]]; then
    FIRST_EPOCH=$(date -d "$FIRST_COMMIT" +%s 2>/dev/null || date -j -f "%Y-%m-%d %H:%M:%S %z" "$FIRST_COMMIT" +%s)
    LAST_EPOCH=$(date -d "$LAST_COMMIT" +%s 2>/dev/null || date -j -f "%Y-%m-%d %H:%M:%S %z" "$LAST_COMMIT" +%s)
    DURATION_MONTHS=$(( ( LAST_EPOCH - FIRST_EPOCH ) / 2592000 )) # 30 days per month
fi

# Analyze commit types (conventional commits)
declare -A COMMIT_TYPES
while IFS= read -r line; do
    if [[ "$line" =~ ^(feat|fix|refactor|perf|test|docs|build|ci|chore|style): ]]; then
        TYPE="${BASH_REMATCH[1]}"
        COMMIT_TYPES[$TYPE]=$((${COMMIT_TYPES[$TYPE]:-0} + 1))
    fi
done < <(git log --author="$AUTHOR" --no-merges --pretty=format:'%s' ${START_DATE:+--since="$START_DATE"} ${END_DATE:+--until="$END_DATE"})

# Get most modified files
MOST_MODIFIED=$(git log --author="$AUTHOR" --no-merges --name-only --pretty=format: ${START_DATE:+--since="$START_DATE"} ${END_DATE:+--until="$END_DATE"} | \
    grep -v '^$' | sort | uniq -c | sort -rn | head -10)

echo -e "${YELLOW}Analysis complete. Generating JSON output...${NC}" >&2

# Output JSON
cat <<EOF
{
  "metadata": {
    "repository": "$REPO_PATH",
    "author": "$AUTHOR",
    "analysis_date": "$(date +%Y-%m-%d)",
    "date_range": {
      "start": "${FIRST_COMMIT%% *}",
      "end": "${LAST_COMMIT%% *}",
      "duration_months": ${DURATION_MONTHS:-0}
    }
  },
  "contribution_summary": {
    "total_commits": $TOTAL_COMMITS,
    "commits_per_month": $(awk "BEGIN {printf \"%.1f\", $TOTAL_COMMITS / ($DURATION_MONTHS > 0 ? $DURATION_MONTHS : 1)}"),
    "total_lines_added": $LINES_ADDED,
    "total_lines_deleted": $LINES_DELETED,
    "net_lines": $NET_LINES,
    "files_modified": $FILES_MODIFIED
  },
  "commit_types": {
$(
    for type in "${!COMMIT_TYPES[@]}"; do
        echo "    \"$type\": ${COMMIT_TYPES[$type]},"
    done | sed '$ s/,$//'
)
  },
  "most_modified_files": [
$(
    echo "$MOST_MODIFIED" | while read -r count file; do
        echo "    {\"file\": \"$file\", \"modifications\": $count},"
    done | sed '$ s/,$//'
)
  ]
}
EOF

echo -e "${GREEN}✓ Commit analysis complete!${NC}" >&2
echo -e "${GREEN}Total commits: $TOTAL_COMMITS | Lines added: $LINES_ADDED | Files modified: $FILES_MODIFIED${NC}" >&2

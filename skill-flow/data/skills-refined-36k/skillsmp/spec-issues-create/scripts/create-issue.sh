#!/bin/bash
# Create GitHub issues from draft markdown files
# Usage: ./create-issue.sh <drafts-directory>

set -e

DRAFTS_DIR="${1:-.}"

# Extract YAML frontmatter field
extract_field() {
  local file="$1"
  local field="$2"
  sed -n '/^---$/,/^---$/p' "$file" | grep "^${field}:" | sed "s/^${field}: *//" | tr -d '"'
}

# Extract body (content after frontmatter)
extract_body() {
  local file="$1"
  sed '1,/^---$/d' "$file" | sed '1,/^---$/d'
}

# Create issue and return number
create_issue() {
  local file="$1"
  local title=$(extract_field "$file" "title")
  local labels=$(extract_field "$file" "labels" | tr -d '[]' | tr ',' ' ')
  local milestone=$(extract_field "$file" "milestone")
  local body=$(extract_body "$file")

  local cmd="gh issue create --title \"$title\" --body \"$body\""

  if [[ -n "$labels" ]]; then
    for label in $labels; do
      label=$(echo "$label" | tr -d '"' | xargs)
      cmd="$cmd --label \"$label\""
    done
  fi

  if [[ -n "$milestone" && "$milestone" != "null" ]]; then
    cmd="$cmd --milestone \"$milestone\""
  fi

  echo "Creating: $title"
  eval "$cmd"
}

# Process all draft files
echo "Processing drafts in: $DRAFTS_DIR"

# Create initiative first (if exists)
for f in "$DRAFTS_DIR"/initiative-*.md; do
  [[ -f "$f" ]] && create_issue "$f"
done

# Then features/tasks
for f in "$DRAFTS_DIR"/issue-*.md; do
  [[ -f "$f" ]] && create_issue "$f"
done

echo "Done!"

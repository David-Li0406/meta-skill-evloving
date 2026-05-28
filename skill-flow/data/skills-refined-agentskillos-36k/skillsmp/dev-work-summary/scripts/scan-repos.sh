#!/bin/bash
# Scans ~/dev recursively for git repos and reports today's work

set -euo pipefail

DEV_DIR="${HOME}/dev"
TODAY_START=$(date +"%Y-%m-%d 00:00:00")
FOUND_WORK=false

echo "🔍 Scanning ${DEV_DIR} for git repositories with activity today..."
echo "📅 Today: $(date +"%Y-%m-%d")"
echo ""

# Find all git repos recursively
while IFS= read -r -d '' git_dir; do
  repo_dir=$(dirname "$git_dir")
  repo_name=$(basename "$repo_dir")

  cd "$repo_dir"

  # Check for commits today
  commits_today=$(git log --since="$TODAY_START" --format="%H" 2>/dev/null | wc -l | tr -d ' ')

  # Check for uncommitted changes
  has_changes=false
  if ! git diff-index --quiet HEAD -- 2>/dev/null || [ -n "$(git ls-files --others --exclude-standard 2>/dev/null)" ]; then
    has_changes=true
  fi

  # Skip if no activity today
  if [ "$commits_today" -eq 0 ] && [ "$has_changes" = false ]; then
    continue
  fi

  FOUND_WORK=true

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📁 ${repo_name}"
  echo "   ${repo_dir}"
  echo ""

  # Current branch
  current_branch=$(git branch --show-current 2>/dev/null || echo "(detached HEAD)")
  echo "🌿 Branch: ${current_branch}"

  # Uncommitted changes
  if [ "$has_changes" = true ]; then
    echo ""
    echo "⚠️  Uncommitted changes:"
    git status --short
  fi

  # Today's commits
  if [ "$commits_today" -gt 0 ]; then
    echo ""
    echo "📝 Commits today (${commits_today}):"
    git log --since="$TODAY_START" --format="%h - %s (%ar)" --reverse

    echo ""
    echo "📊 Stats:"
    git log --since="$TODAY_START" --stat --format="" | tail -n 1

    echo ""
    echo "🔎 What was done:"
    # Get detailed analysis from diffs
    git log --since="$TODAY_START" --format="" --reverse | while IFS= read -r line; do
      if [[ "$line" =~ ^diff ]]; then
        echo "  • $line"
      fi
    done

    # Analyze commit diffs for better understanding
    git log --since="$TODAY_START" --format="%H" --reverse | while read -r commit; do
      echo ""
      echo "  Commit: $(git log -1 --format="%s" "$commit")"
      git diff-tree --no-commit-id --name-status -r "$commit" | while read -r status file; do
        case "$status" in
          A) echo "    ✅ Added: $file" ;;
          M) echo "    ✏️  Modified: $file" ;;
          D) echo "    ❌ Deleted: $file" ;;
          R*) echo "    ➡️  Renamed: $file" ;;
        esac
      done
    done
  fi

  echo ""
done < <(find "$DEV_DIR" -type d -name ".git" -print0 2>/dev/null)

if [ "$FOUND_WORK" = false ]; then
  echo "✨ No activity found in ${DEV_DIR} today"
  echo ""
  echo "Repos scanned: $(find "$DEV_DIR" -type d -name ".git" 2>/dev/null | wc -l | tr -d ' ')"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Scan complete"

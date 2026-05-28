#!/bin/bash
# Daily Git Summary Script
# Scans all git repos under ~/dev and reports commits for a given date
# Usage: daily-git-summary.sh [YYYY-MM-DD]
#
# Output: Logs saved to ~/logs/daily/raw/YYYY-MM-DDTHH-MM-SS-daily-github-summary.md
# State: Tracks repos in ~/.local/state/daily-repos.txt

DATE="${1:-$(date +%Y-%m-%d)}"
DEV_DIR="${2:-$HOME/dev}"

# Setup logging
LOG_DIR="${HOME}/logs/daily/raw"
TIMESTAMP=$(date +%Y-%m-%dT%H-%M-%S)
LOG_FILE="${LOG_DIR}/${TIMESTAMP}-daily-github-summary.md"
mkdir -p "$LOG_DIR"

# Setup state tracking
STATE_DIR="${HOME}/.local/state"
STATE_FILE="${STATE_DIR}/daily-repos.txt"
mkdir -p "$STATE_DIR"

# Use exec to redirect all output to both terminal and log file
exec > >(tee "$LOG_FILE") 2>&1

# Get current list of repos
CURRENT_REPOS=$(find "$DEV_DIR" -type d -name ".git" 2>/dev/null | sed 's|/.git$||' | sed "s|$DEV_DIR/||" | sort)

echo "=== Repository Changes ==="
echo ""

# Compare with previous state
if [ -f "$STATE_FILE" ]; then
  PREVIOUS_REPOS=$(cat "$STATE_FILE" | sort)

  # Find added repos (in current but not in previous)
  ADDED=$(comm -23 <(echo "$CURRENT_REPOS") <(echo "$PREVIOUS_REPOS"))

  # Find removed repos (in previous but not in current)
  REMOVED=$(comm -13 <(echo "$CURRENT_REPOS") <(echo "$PREVIOUS_REPOS"))

  if [ -n "$ADDED" ]; then
    echo "### Repos Added"
    echo "$ADDED" | while read repo; do
      echo "- $repo"
    done
    echo ""
  fi

  if [ -n "$REMOVED" ]; then
    echo "### Repos Removed"
    echo "$REMOVED" | while read repo; do
      echo "- $repo"
    done
    echo ""
  fi

  if [ -z "$ADDED" ] && [ -z "$REMOVED" ]; then
    echo "No repository changes"
    echo ""
  fi
else
  echo "First run - tracking $(echo "$CURRENT_REPOS" | wc -l | tr -d ' ') repositories"
  echo ""
fi

# Update state file
echo "$CURRENT_REPOS" > "$STATE_FILE"

echo "=== Git Activity for $DATE ==="
echo ""

# Get repo visibility from GitHub API
get_repo_visibility() {
  local repo_name="$1"
  local visibility
  visibility=$(gh repo view "$repo_name" --json visibility --jq '.visibility' 2>/dev/null | tr '[:upper:]' '[:lower:]')
  if [ -n "$visibility" ]; then
    echo "$visibility"
  else
    echo "local"
  fi
}

# Find all git repos and check for commits
while IFS= read -r gitdir; do
  repo=$(dirname "$gitdir")
  repo_name=$(echo "$repo" | sed "s|$HOME/dev/||")

  # Get author email from repo's git config
  author_email=$(cd "$repo" && git config user.email 2>/dev/null)

  # Get commits for the date, filtered by author
  commits=$(cd "$repo" && git log --oneline --author="$author_email" --since="$DATE 00:00:00" --until="$DATE 23:59:59" 2>/dev/null)

  if [ -n "$commits" ]; then
    count=$(echo "$commits" | wc -l)
    visibility=$(get_repo_visibility "$repo_name")
    echo "### $repo_name ($visibility) - $count commits"
    echo "$commits"
    echo ""
  fi
done < <(find "$DEV_DIR" -type d -name ".git" 2>/dev/null | sort)

echo "=== GitHub Activity ==="
echo ""

# Check if gh is available
if command -v gh &> /dev/null; then
  # Issues created by me today
  echo "### Issues Created"
  issues_created=$(gh search issues --author=@me --created="$DATE" --limit=20 \
    --json repository,number,title \
    --jq '.[] | "- " + .repository.nameWithOwner + "#" + (.number|tostring) + ": " + .title' 2>/dev/null)
  if [ -n "$issues_created" ]; then
    echo "$issues_created"
  else
    echo "None"
  fi
  echo ""

  # Issues closed today (that involve me)
  echo "### Issues Closed"
  issues_closed=$(gh search issues --involves=@me --closed="$DATE" --limit=20 \
    --json repository,number,title \
    --jq '.[] | "- " + .repository.nameWithOwner + "#" + (.number|tostring) + ": " + .title' 2>/dev/null)
  if [ -n "$issues_closed" ]; then
    echo "$issues_closed"
  else
    echo "None"
  fi
  echo ""

  # PRs opened by me today
  echo "### PRs Opened"
  prs_opened=$(gh search prs --author=@me --created="$DATE" --limit=20 \
    --json repository,number,title \
    --jq '.[] | "- " + .repository.nameWithOwner + "#" + (.number|tostring) + ": " + .title' 2>/dev/null)
  if [ -n "$prs_opened" ]; then
    echo "$prs_opened"
  else
    echo "None"
  fi
  echo ""

  # PRs merged today (that I authored)
  echo "### PRs Merged"
  prs_merged=$(gh search prs --author=@me --merged="$DATE" --limit=20 \
    --json repository,number,title \
    --jq '.[] | "- " + .repository.nameWithOwner + "#" + (.number|tostring) + ": " + .title' 2>/dev/null)
  if [ -n "$prs_merged" ]; then
    echo "$prs_merged"
  else
    echo "None"
  fi
  echo ""

  # === Activity from Events API ===
  echo "=== Activity from Events API ==="
  echo ""

  # Get all events and filter by date
  # Events API returns ISO timestamps, we filter for the target date
  # Note: @me doesn't work for events API, need to get username
  GH_USER=$(gh api /user --jq '.login' 2>/dev/null)
  EVENTS=$(gh api "/users/${GH_USER}/events" --paginate 2>/dev/null)

  # PR Reviews
  echo "### PR Reviews"
  pr_reviews=$(echo "$EVENTS" | jq -r --arg date "$DATE" '
    .[] | select(.type == "PullRequestReviewEvent") |
    select(.created_at | startswith($date)) |
    "- " + .repo.name + "#" + (.payload.pull_request.number|tostring) + ": " + .payload.review.state + " - " + .payload.pull_request.title
  ' 2>/dev/null)
  if [ -n "$pr_reviews" ]; then
    echo "$pr_reviews"
  else
    echo "None"
  fi
  echo ""

  # Issue Comments
  echo "### Issue Comments"
  issue_comments=$(echo "$EVENTS" | jq -r --arg date "$DATE" '
    .[] | select(.type == "IssueCommentEvent") |
    select(.created_at | startswith($date)) |
    "- " + .repo.name + "#" + (.payload.issue.number|tostring) + ": " + (.payload.comment.body | split("\n")[0] | if length > 60 then .[0:60] + "..." else . end)
  ' 2>/dev/null)
  if [ -n "$issue_comments" ]; then
    echo "$issue_comments"
  else
    echo "None"
  fi
  echo ""

  # PR Comments (review comments)
  echo "### PR Comments"
  pr_comments=$(echo "$EVENTS" | jq -r --arg date "$DATE" '
    .[] | select(.type == "PullRequestReviewCommentEvent") |
    select(.created_at | startswith($date)) |
    "- " + .repo.name + "#" + (.payload.pull_request.number|tostring) + ": " + (.payload.comment.body | split("\n")[0] | if length > 60 then .[0:60] + "..." else . end)
  ' 2>/dev/null)
  if [ -n "$pr_comments" ]; then
    echo "$pr_comments"
  else
    echo "None"
  fi
  echo ""

  # Repos forked today
  echo "### Repos Forked"
  repos_forked=$(echo "$EVENTS" | jq -r --arg date "$DATE" '
    .[] | select(.type == "ForkEvent") |
    select(.created_at | startswith($date)) |
    "- " + .repo.name + " -> " + .payload.forkee.full_name
  ' 2>/dev/null)
  if [ -n "$repos_forked" ]; then
    echo "$repos_forked"
  else
    echo "None"
  fi
  echo ""

  # Branches/tags created
  echo "### Branches/Tags Created"
  refs_created=$(echo "$EVENTS" | jq -r --arg date "$DATE" '
    .[] | select(.type == "CreateEvent") |
    select(.created_at | startswith($date)) |
    "- " + .repo.name + ": " + .payload.ref_type + " " + (.payload.ref // "(default branch)")
  ' 2>/dev/null)
  if [ -n "$refs_created" ]; then
    echo "$refs_created"
  else
    echo "None"
  fi
  echo ""

  # Push events to repos NOT in ~/dev (external contributions)
  echo "### External Pushes (repos not in ~/dev)"
  LOCAL_REPOS=$(find "$DEV_DIR" -type d -name ".git" 2>/dev/null | sed 's|/.git$||' | sed "s|$DEV_DIR/||" | sort)
  external_pushes=$(echo "$EVENTS" | jq -r --arg date "$DATE" '
    .[] | select(.type == "PushEvent") |
    select(.created_at | startswith($date)) |
    .repo.name
  ' 2>/dev/null | sort -u | while read repo; do
    # Check if repo exists locally
    if ! echo "$LOCAL_REPOS" | grep -q "^${repo}$"; then
      echo "- $repo"
    fi
  done)
  if [ -n "$external_pushes" ]; then
    echo "$external_pushes"
  else
    echo "None"
  fi
else
  echo "gh CLI not available - skipping GitHub activity"
fi

echo ""
echo "=== End of Summary ==="
echo ""
echo "Log saved: $LOG_FILE"

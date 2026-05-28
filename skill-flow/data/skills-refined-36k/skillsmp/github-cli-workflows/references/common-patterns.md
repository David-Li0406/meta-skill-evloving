# Common Patterns

Reusable patterns and best practices for GitHub CLI operations.

## Authentication Verification

### Check Authentication Status

**Pattern: Verify authentication without error if not authenticated**

```bash
if gh auth status &>/dev/null; then
  echo "Authenticated"
else
  echo "Not authenticated. Run: gh auth login"
fi
```

**Get authenticated user:**
```bash
gh api user --jq '.login'
```

**Check token scopes:**
```bash
gh auth status --show-token 2>&1 | grep "Token scopes:"
```

### Authentication Recovery

When authentication fails:

```bash
# Check current status
gh auth status

# If not authenticated, login
gh auth login

# For Enterprise
gh auth login --hostname github.company.com

# Login with specific scopes
gh auth login --scopes repo,workflow,admin:org
```

## Repository Context

### Verify Repository Context

**Pattern: Ensure we're in a repository with correct context**

```bash
# Check if in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "Error: Not in a git repository"
  exit 1
fi

# Verify GitHub CLI can access repository
if ! gh repo view &>/dev/null; then
  echo "Error: Cannot access repository via GitHub CLI"
  exit 1
fi

# Get repository details
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
echo "Working with repository: $REPO"
```

### Extract Repository Information

```bash
# Get owner and repo
OWNER=$(gh repo view --json owner --jq '.owner.login')
REPO_NAME=$(gh repo view --json name --jq '.name')

# Get current branch
BRANCH=$(git branch --show-current)

# Get default branch
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name')

# Check if repository is private
IS_PRIVATE=$(gh repo view --json isPrivate --jq '.isPrivate')
```

## Error Handling

### Standard Error Handling Pattern

```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined variables, pipe failures

# Function for error handling
handle_error() {
  local exit_code=$?
  local line_number=$1
  echo "Error on line $line_number (exit code: $exit_code)"
  exit $exit_code
}

trap 'handle_error $LINENO' ERR

# Your gh commands here
gh pr list
```

### Retry Pattern for Transient Failures

```bash
retry() {
  local max_attempts=3
  local delay=5
  local attempt=1

  while [ $attempt -le $max_attempts ]; do
    if "$@"; then
      return 0
    else
      echo "Attempt $attempt failed. Retrying in ${delay}s..."
      sleep $delay
      attempt=$((attempt + 1))
    fi
  done

  echo "Command failed after $max_attempts attempts"
  return 1
}

# Usage
retry gh pr list
```

### Graceful Failure Pattern

```bash
# Try operation, fallback on failure
if ! OUTPUT=$(gh pr view 123 2>&1); then
  echo "Warning: Could not fetch PR details: $OUTPUT"
  echo "Continuing with limited information..."
  # Fallback logic here
else
  # Process successful output
  echo "$OUTPUT"
fi
```

## Working with JSON

### Parse and Extract Data

**Pattern: Fetch JSON, extract fields, format for display**

```bash
# Get PR data
PR_DATA=$(gh pr view 123 --json number,title,author,state,createdAt)

# Extract fields
PR_TITLE=$(echo "$PR_DATA" | jq -r '.title')
PR_AUTHOR=$(echo "$PR_DATA" | jq -r '.author.login')
PR_STATE=$(echo "$PR_DATA" | jq -r '.state')

# Format for display
echo "PR #123: $PR_TITLE"
echo "Author: $PR_AUTHOR"
echo "State: $PR_STATE"
```

### Process Arrays

```bash
# Get list of open PRs
gh pr list --state open --json number,title \
  | jq -r '.[] | "#\(.number): \(.title)"'

# Filter and count
LABEL_COUNT=$(gh issue list --label bug --json number | jq 'length')
echo "Open bugs: $LABEL_COUNT"

# Group and aggregate
gh issue list --json labels --jq '
  [.[].labels[].name]
  | group_by(.)
  | map({label: .[0], count: length})
  | sort_by(.count)
  | reverse
'
```

### Combine Multiple Queries

```bash
# Get PR with review status
PR=123
PR_INFO=$(gh pr view $PR --json number,title,state)
REVIEWS=$(gh api repos/{owner}/{repo}/pulls/$PR/reviews --jq '[.[] | {author: .user.login, state: .state}]')

# Combine into single JSON
jq -n \
  --argjson pr "$PR_INFO" \
  --argjson reviews "$REVIEWS" \
  '{"pr": $pr, "reviews": $reviews}'
```

## Batch Operations

### Process Multiple Items

**Pattern: Safe batch processing with error handling**

```bash
#!/bin/bash

process_issues() {
  local issues=("$@")
  local success_count=0
  local failure_count=0

  for issue in "${issues[@]}"; do
    echo "Processing issue #$issue..."

    if gh issue edit "$issue" --add-label processed; then
      echo "✓ Successfully processed #$issue"
      ((success_count++))
    else
      echo "✗ Failed to process #$issue"
      ((failure_count++))
    fi
  done

  echo ""
  echo "Summary: $success_count succeeded, $failure_count failed"
}

# Usage
ISSUE_LIST=(123 124 125 126)
process_issues "${ISSUE_LIST[@]}"
```

### Parallel Processing

```bash
# Process items in parallel (be careful with rate limits)
gh pr list --json number --jq '.[].number' \
  | xargs -P 5 -I {} bash -c 'gh pr checks {} --json name,status,conclusion'

# With GNU parallel (if available)
gh pr list --json number --jq '.[].number' \
  | parallel -j 5 'gh pr checks {}'
```

### Rate Limit Aware Batching

```bash
check_rate_limit() {
  local remaining=$(gh api rate_limit --jq '.rate.remaining')
  local limit=$(gh api rate_limit --jq '.rate.limit')
  local reset=$(gh api rate_limit --jq '.rate.reset')

  if [ "$remaining" -lt 100 ]; then
    local now=$(date +%s)
    local wait=$((reset - now + 10))  # Add 10s buffer
    echo "Rate limit low ($remaining/$limit). Waiting ${wait}s..."
    sleep $wait
  fi
}

# Use in batch operations
for issue in $(gh issue list --json number --jq '.[].number'); do
  check_rate_limit
  gh issue edit "$issue" --add-label processed
done
```

## State Management

### Save State for Long Operations

```bash
#!/bin/bash

STATE_FILE=".gh-operation-state"

save_state() {
  echo "$1" > "$STATE_FILE"
}

load_state() {
  if [ -f "$STATE_FILE" ]; then
    cat "$STATE_FILE"
  else
    echo ""
  fi
}

clear_state() {
  rm -f "$STATE_FILE"
}

# Usage in a script
LAST_PROCESSED=$(load_state)

gh issue list --json number --jq '.[].number' \
  | while read issue; do
    # Skip already processed
    if [ -n "$LAST_PROCESSED" ] && [ "$issue" -le "$LAST_PROCESSED" ]; then
      continue
    fi

    # Process issue
    gh issue edit "$issue" --add-label automated

    # Save progress
    save_state "$issue"
  done

clear_state
```

## Confirmation Prompts

### User Confirmation Pattern

```bash
confirm() {
  local prompt="${1:-Are you sure?}"
  local response

  read -r -p "$prompt [y/N] " response
  case "$response" in
    [yY][eE][sS]|[yY])
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

# Usage
if confirm "Close issue #123?"; then
  gh issue close 123
else
  echo "Cancelled"
fi
```

### Dry-Run Pattern

```bash
DRY_RUN=false

execute() {
  local cmd="$1"

  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Would execute: $cmd"
  else
    eval "$cmd"
  fi
}

# Usage
# DRY_RUN=true ./script.sh  # See what would happen
# ./script.sh               # Actually execute

execute "gh issue close 123"
execute "gh pr merge 456 --squash"
```

## Multi-Repository Operations

### Iterate Over Repositories

```bash
# Get all repositories for user
gh repo list --limit 100 --json name \
  | jq -r '.[].name' \
  | while read repo; do
    echo "Processing $repo..."
    gh -R "$(gh api user --jq '.login')/$repo" issue list --label bug
  done

# Process repositories matching pattern
gh repo list --limit 1000 --json nameWithOwner \
  | jq -r '.[] | select(.nameWithOwner | contains("backend")) | .nameWithOwner' \
  | while read repo; do
    echo "Checking $repo..."
    gh -R "$repo" pr list --state open
  done
```

### Clone Multiple Repositories

```bash
# Clone all repositories for an org
ORG="myorg"
gh repo list "$ORG" --limit 1000 --json name \
  | jq -r '.[].name' \
  | while read repo; do
    gh repo clone "$ORG/$repo"
  done
```

## Working with Draft PRs

### Create Draft, Then Mark Ready

```bash
# Create draft PR
PR_NUMBER=$(gh pr create \
  --draft \
  --title "WIP: Feature X" \
  --body "Work in progress" \
  --json number --jq '.number')

# Do work...
echo "Implementing feature..."

# Mark ready for review
gh pr ready "$PR_NUMBER"
gh pr edit "$PR_NUMBER" --add-reviewer alice,bob
```

### Convert Ready to Draft

```bash
gh pr ready 123 --undo
```

## Label Management

### Sync Labels Across Repositories

```bash
SOURCE_REPO="org/template-repo"
TARGET_REPO="org/new-repo"

# Get labels from source
LABELS=$(gh -R "$SOURCE_REPO" label list --json name,description,color)

# Create in target
echo "$LABELS" | jq -c '.[]' | while read label; do
  NAME=$(echo "$label" | jq -r '.name')
  DESC=$(echo "$label" | jq -r '.description')
  COLOR=$(echo "$label" | jq -r '.color')

  gh -R "$TARGET_REPO" label create "$NAME" \
    --description "$DESC" \
    --color "$COLOR" 2>/dev/null || echo "Label $NAME already exists"
done
```

### Auto-Label Based on Content

```bash
auto_label_issue() {
  local issue=$1
  local title=$(gh issue view "$issue" --json title --jq '.title')
  local body=$(gh issue view "$issue" --json body --jq '.body')
  local content="$title $body"

  # Add labels based on content
  if echo "$content" | grep -qi "bug\|error\|crash"; then
    gh issue edit "$issue" --add-label bug
  fi

  if echo "$content" | grep -qi "feature\|enhancement"; then
    gh issue edit "$issue" --add-label enhancement
  fi

  if echo "$content" | grep -qi "documentation\|docs"; then
    gh issue edit "$issue" --add-label documentation
  fi
}

# Apply to new issues
gh issue list --label needs-triage --json number \
  | jq -r '.[].number' \
  | while read issue; do
    auto_label_issue "$issue"
    gh issue edit "$issue" --remove-label needs-triage
  done
```

## CI/CD Integration

### Wait for Checks to Complete

```bash
wait_for_checks() {
  local pr=$1
  local timeout=1800  # 30 minutes
  local elapsed=0
  local interval=30

  echo "Waiting for checks on PR #$pr..."

  while [ $elapsed -lt $timeout ]; do
    # Get check status
    CHECKS=$(gh pr checks "$pr" --json name,status,conclusion)

    # Check if all complete
    IN_PROGRESS=$(echo "$CHECKS" | jq '[.[] | select(.status != "COMPLETED")] | length')

    if [ "$IN_PROGRESS" -eq 0 ]; then
      # All checks complete, check conclusion
      FAILED=$(echo "$CHECKS" | jq '[.[] | select(.conclusion != "SUCCESS")] | length')

      if [ "$FAILED" -eq 0 ]; then
        echo "All checks passed!"
        return 0
      else
        echo "Some checks failed"
        echo "$CHECKS" | jq '.[] | select(.conclusion != "SUCCESS")'
        return 1
      fi
    fi

    sleep $interval
    elapsed=$((elapsed + interval))
    echo "Still waiting... ($elapsed/${timeout}s)"
  done

  echo "Timeout waiting for checks"
  return 1
}

# Usage
if wait_for_checks 123; then
  gh pr merge 123 --squash
fi
```

### Trigger Workflow and Wait

```bash
trigger_and_wait() {
  local workflow=$1
  shift
  local args=("$@")

  # Trigger workflow
  gh workflow run "$workflow" "${args[@]}"

  # Wait a bit for run to start
  sleep 10

  # Get most recent run
  RUN_ID=$(gh run list --workflow "$workflow" --limit 1 --json databaseId --jq '.[0].databaseId')

  # Watch run
  gh run watch "$RUN_ID" --exit-status
}

# Usage
trigger_and_wait deploy.yml --ref main --field environment=production
```

## Template-Based Operations

### Use Issue Templates

```bash
# Create issue from template with variable substitution
create_from_template() {
  local template=$1
  local title=$2
  shift 2
  local vars=("$@")

  # Read template
  local body=$(cat ".github/ISSUE_TEMPLATE/$template")

  # Substitute variables
  for var in "${vars[@]}"; do
    local key=$(echo "$var" | cut -d= -f1)
    local value=$(echo "$var" | cut -d= -f2)
    body=$(echo "$body" | sed "s/{{$key}}/$value/g")
  done

  # Create issue
  gh issue create --title "$title" --body "$body"
}

# Usage
create_from_template bug_report.md \
  "Bug in feature X" \
  "VERSION=2.0.0" \
  "COMPONENT=auth"
```

## Cleanup Operations

### Archive Old Branches

```bash
# Delete merged branches (except main/develop)
gh api repos/{owner}/{repo}/branches --paginate \
  | jq -r '.[] | select(.name != "main" and .name != "develop") | .name' \
  | while read branch; do
    # Check if branch is merged
    if git branch -r --merged origin/main | grep -q "origin/$branch"; then
      echo "Deleting merged branch: $branch"
      git push origin --delete "$branch" || echo "Could not delete $branch"
    fi
  done
```

### Close Stale Issues and PRs

```bash
DAYS=60
CUTOFF=$(date -d "$DAYS days ago" +%Y-%m-%d)

# Close stale issues
gh issue list --json number,title,updatedAt \
  --jq ".[] | select(.updatedAt < \"$CUTOFF\")" \
  | jq -r '.number' \
  | while read issue; do
    gh issue close "$issue" \
      --comment "Closing due to inactivity (>$DAYS days). Please reopen if still relevant."
  done

# Close stale PRs
gh pr list --json number,title,updatedAt \
  --jq ".[] | select(.updatedAt < \"$CUTOFF\")" \
  | jq -r '.number' \
  | while read pr; do
    gh pr close "$pr" \
      --comment "Closing due to inactivity (>$DAYS days). Please reopen if still relevant."
  done
```

## Best Practices Summary

1. **Always verify authentication and repository context** before operations
2. **Use JSON output for programmatic processing**, format for humans in display
3. **Implement error handling and retry logic** for resilience
4. **Check rate limits** before batch operations
5. **Use confirmation prompts** for destructive operations
6. **Save state** for long-running operations
7. **Provide dry-run mode** for testing workflows
8. **Handle pagination** for complete datasets
9. **Use parallel processing** carefully (watch rate limits)
10. **Clean up resources** (branches, old runs, artifacts) regularly

## Script Template

**Complete script template with best practices:**

```bash
#!/bin/bash
set -euo pipefail

# Configuration
DRY_RUN=${DRY_RUN:-false}
VERBOSE=${VERBOSE:-false}

# Error handling
handle_error() {
  echo "Error on line $1" >&2
  exit 1
}
trap 'handle_error $LINENO' ERR

# Logging
log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

verbose() {
  if [ "$VERBOSE" = true ]; then
    echo "[DEBUG] $*"
  fi
}

# Check authentication
if ! gh auth status &>/dev/null; then
  echo "Error: Not authenticated. Run: gh auth login"
  exit 1
fi

# Check repository context
if ! gh repo view &>/dev/null; then
  echo "Error: Not in a GitHub repository"
  exit 1
fi

# Your main logic here
main() {
  log "Starting operation..."

  # Example: List issues
  gh issue list --json number,title \
    | jq -r '.[] | "#\(.number): \(.title)"'

  log "Operation complete"
}

# Run main
main "$@"
```

## Related Resources

- `pr-workflows.md` - PR-specific patterns
- `issue-workflows.md` - Issue-specific patterns
- `actions-workflows.md` - CI/CD patterns
- `api-usage.md` - Advanced API operations

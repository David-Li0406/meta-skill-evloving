# Batch Mode Processing

Process multiple Linear issues efficiently.

## Fetching Multiple Issues

```bash
# Get issues assigned to user
ISSUES=$(linear issue list --team ARB --state "Todo" --assignee luke --json | \
  jq -r '.[].identifier')

# Get issues by filter
linear issue list --team SIP --state "In Progress" --json | \
  jq -r '.[].identifier'

# Search by keyword
linear issue search --query "auth" --limit 20 --json | \
  jq -r '.[].identifier'
```

## Processing Loop

```bash
for issue in $ISSUES; do
  echo "=== Processing $issue ==="

  # Optional: skip if issue-context already posted
  if linear comment list "$issue" --json | jq -r '.[].body' | rg -q "issue-context:"; then
    echo "Skipping $issue (already has issue-context)"
    continue
  fi

  # 1. View issue
  linear issue view "$issue"

  # 2. Run git audit for this issue area
  # git log --grep="$issue" --oneline

  # 3. Run outline/layer analysis
  # Based on issue keywords

  # 4. Generate comments
  # Create ANALYSIS and AGENT_PROMPT variables

  # 5. Post comments (set DRY_RUN=1 to skip)
  if [ "${DRY_RUN:-0}" -eq 1 ]; then
    echo "DRY RUN: would post comments for $issue"
  else
    linear comment create -i "$issue" -b "$ANALYSIS"
    linear comment create -i "$issue" -b "$AGENT_PROMPT"
  fi

  sleep 1  # Rate limiting
done
```

## Optimizations

### Cache outline results
```bash
# Use -c flag for caching
fd -e ts . src | outline -c --format=yaml
```

### Share layer diagrams
For issues in same codebase area, generate once:
```bash
layer . --format=mermaid -o /tmp/architecture.md
# Reference in multiple issue comments
```

### Group by module
```bash
# Sort issues by affected area
for area in auth api ui; do
  echo "=== $area issues ==="
  # Process issues related to this area together
done
```

### One-time git audit
```bash
# Run comprehensive git audit once
git log --oneline --since="4 weeks ago" --all > /tmp/git-audit.txt

# Reference per-issue
grep -i "$KEYWORD" /tmp/git-audit.txt
```

## Rate Limiting

```bash
# Add delay between API calls
sleep 1

# Or use xargs with parallel limit
echo "$ISSUES" | xargs -P 2 -I {} process_issue {}
```

## Error Handling

```bash
for issue in $ISSUES; do
  if ! linear issue view "$issue" --json > /dev/null 2>&1; then
    echo "WARN: Could not fetch $issue, skipping"
    continue
  fi

  # Process issue...

  if ! linear comment create -i "$issue" -b "$COMMENT"; then
    echo "ERROR: Failed to post comment to $issue"
  fi
done
```

## Progress Tracking

```bash
TOTAL=$(echo "$ISSUES" | wc -w)
COUNT=0

for issue in $ISSUES; do
  COUNT=$((COUNT + 1))
  echo "[$COUNT/$TOTAL] Processing $issue..."

  # Process...

  echo "[$COUNT/$TOTAL] Done: $issue"
done

echo "Completed $COUNT issues"
```

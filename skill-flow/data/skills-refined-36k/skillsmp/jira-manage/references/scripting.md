# Scripting and Automation

Examples for automating Jira operations and CI/CD integration.

## Output Formats for Scripts

Always use `--plain` for scripted operations:

```bash
# Plain text (default for scripts)
jira issue list --plain

# CSV format
jira issue list --csv

# Raw JSON
jira issue list --raw

# Custom columns, no headers
jira issue list --plain --columns key,summary,status --no-headers
```

## Bash Patterns

### Extract Issue Keys

```bash
# Get list of issue keys
keys=$(jira issue list -a$(jira me) --plain --columns key --no-headers)

# Process each key
for key in $keys; do
  echo "Processing $key"
  jira issue view "$key" --plain
done
```

### Tickets Created Per Day

```bash
#!/usr/bin/env bash

tickets=$(jira issue list --created month --plain --columns created --no-headers | \
  awk '{print $2}' | awk -F'-' '{print $3}' | sort -n | uniq -c)

echo "${tickets}" | while IFS=$'\t' read -r line; do
  day=$(echo "${line}" | awk '{print $2}')
  count=$(echo "${line}" | awk '{print $1}')
  printf "Day #%s: %s tickets\n" "${day}" "${count}"
done
```

### Tickets Per Sprint

```bash
#!/usr/bin/env bash

sprints=$(jira sprint list --table --plain --columns id,name --no-headers)

echo "${sprints}" | while IFS=$'\t' read -r id name; do
  count=$(jira sprint list "${id}" --plain --no-headers 2>/dev/null | wc -l)
  printf "%10s: %3d tickets\n" "${name}" $((count))
done
```

### Sprint Report

```bash
#!/usr/bin/env bash

SPRINT_ID=$1

if [ -z "$SPRINT_ID" ]; then
  echo "Usage: $0 <sprint-id>"
  exit 1
fi

echo "=== Sprint Report for Sprint $SPRINT_ID ==="

total=$(jira sprint list "$SPRINT_ID" --plain --no-headers | wc -l)
done_count=$(jira sprint list "$SPRINT_ID" -sDone --plain --no-headers | wc -l)
in_progress=$(jira sprint list "$SPRINT_ID" -s"In Progress" --plain --no-headers | wc -l)
todo=$(jira sprint list "$SPRINT_ID" -s"To Do" --plain --no-headers | wc -l)

echo "Total: $total"
echo "Done: $done_count"
echo "In Progress: $in_progress"
echo "To Do: $todo"

if [ "$total" -gt 0 ]; then
  completion=$(echo "scale=1; ($done_count / $total) * 100" | bc)
  echo "Completion: ${completion}%"
fi
```

### Bulk Assignment (Round Robin)

```bash
#!/usr/bin/env bash

issues=$(jira issue list -ax -yHigh -s"To Do" --plain --columns key --no-headers)
team=("alice" "bob" "charlie")
team_size=${#team[@]}
index=0

for issue in $issues; do
  assignee="${team[$index]}"
  echo "Assigning $issue to $assignee"
  jira issue assign "$issue" "$assignee"
  index=$(( (index + 1) % team_size ))
done
```

### Export to CSV

```bash
#!/usr/bin/env bash

OUTPUT_FILE="issues_$(date +%Y%m%d).csv"

jira issue list \
  --created month \
  --csv \
  --columns key,type,status,priority,assignee,summary,created \
  > "$OUTPUT_FILE"

echo "Exported to $OUTPUT_FILE"
```

### Monitor High Priority Issues

```bash
#!/usr/bin/env bash

THRESHOLD=5
count=$(jira issue list -ax -yHigh -s~Done --plain --no-headers | wc -l)

if [ "$count" -gt "$THRESHOLD" ]; then
  echo "Alert: $count high priority unassigned issues"
  jira issue list -ax -yHigh -s~Done --plain --columns key,summary
  exit 1
else
  echo "OK: $count high priority unassigned issues"
fi
```

### Stale Issue Cleanup

```bash
#!/usr/bin/env bash

# Find issues not updated in 3 months
stale=$(jira issue list --updated-before -12w -s"To Do" --plain --columns key --no-headers)

for key in $stale; do
  echo "Stale: $key"
  jira issue comment add "$key" "This issue hasn't been updated in 3 months. Still relevant?"
  jira issue edit "$key" --label stale --no-input
done
```

## CI/CD Integration

### GitHub Actions - Create Issue on PR

```yaml
name: Create Jira Issue
on:
  pull_request:
    types: [opened]

jobs:
  create-jira:
    runs-on: ubuntu-latest
    steps:
      - name: Install jira-cli
        run: |
          wget https://github.com/ankitpokhrel/jira-cli/releases/latest/download/jira_linux_amd64.tar.gz
          tar -xf jira_linux_amd64.tar.gz
          sudo mv jira /usr/local/bin/

      - name: Create Jira Issue
        env:
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
        run: |
          jira issue create \
            -tTask \
            -s"Review PR #${{ github.event.pull_request.number }}: ${{ github.event.pull_request.title }}" \
            -b"${{ github.event.pull_request.html_url }}" \
            --no-input
```

### GitHub Actions - Update Jira on Merge

```yaml
name: Update Jira on Merge
on:
  pull_request:
    types: [closed]

jobs:
  update-jira:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Install jira-cli
        run: |
          wget https://github.com/ankitpokhrel/jira-cli/releases/latest/download/jira_linux_amd64.tar.gz
          tar -xf jira_linux_amd64.tar.gz
          sudo mv jira /usr/local/bin/

      - name: Extract Jira Keys and Update
        env:
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
        run: |
          # Extract Jira keys from PR title/commits
          KEYS=$(echo "${{ github.event.pull_request.title }}" | grep -oE '[A-Z]+-[0-9]+' || true)

          for KEY in $KEYS; do
            echo "Updating $KEY"
            jira issue move "$KEY" Done -RFixed --comment "Merged in PR #${{ github.event.pull_request.number }}"
          done
```

### GitLab CI - Update on Deploy

```yaml
update_jira:
  stage: deploy
  script:
    - |
      # Extract Jira keys from commit messages
      JIRA_KEYS=$(git log --format=%B -n 10 | grep -oE '[A-Z]+-[0-9]+' | sort -u)

      for KEY in $JIRA_KEYS; do
        echo "Updating $KEY"
        jira issue move "$KEY" Done -RDeployed --comment "Deployed to production"
      done
  only:
    - main
```

## Git Hooks

### Pre-commit: Validate Branch Name

```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit

branch=$(git rev-parse --abbrev-ref HEAD)
jira_key=$(echo "$branch" | grep -oE '^[A-Z]+-[0-9]+' || true)

if [ -z "$jira_key" ]; then
  echo "Warning: Branch name doesn't start with Jira key (e.g., PROJ-123-feature)"
fi
```

### Commit-msg: Add Jira Key

```bash
#!/usr/bin/env bash
# .git/hooks/commit-msg

branch=$(git rev-parse --abbrev-ref HEAD)
jira_key=$(echo "$branch" | grep -oE '^[A-Z]+-[0-9]+' || true)

if [ -n "$jira_key" ]; then
  # Prepend Jira key if not already present
  if ! grep -qE "^$jira_key" "$1"; then
    sed -i.bak "1s/^/$jira_key: /" "$1"
  fi
fi
```

## Error Handling

```bash
#!/usr/bin/env bash
set -euo pipefail

# Check if jira-cli is available
if ! command -v jira &> /dev/null; then
  echo "Error: jira-cli not found"
  exit 1
fi

# Check for required environment
if [ -z "${JIRA_API_TOKEN:-}" ]; then
  echo "Error: JIRA_API_TOKEN not set"
  exit 1
fi

# Wrap commands with error handling
if ! output=$(jira issue list -a$(jira me) --plain 2>&1); then
  echo "Error fetching issues: $output"
  exit 1
fi
```

## Rate Limiting

```bash
#!/usr/bin/env bash

issues=$(jira issue list --plain --columns key --no-headers)

for issue in $issues; do
  echo "Processing $issue"
  jira issue view "$issue" > /dev/null

  # Rate limit: 1 request per second
  sleep 1
done
```

## JSON Processing

```bash
# Get raw JSON and process with jq
jira issue list --raw | jq '.issues[] | {key: .key, summary: .fields.summary}'

# Extract specific fields
jira issue list --raw | jq -r '.issues[] | "\(.key)\t\(.fields.status.name)"'
```

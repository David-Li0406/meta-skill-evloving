# Linear CLI Patterns

Common Linear CLI patterns for linear-audit.

---

## workspaces

| workspace | teams | flag |
|-----------|-------|------|
| luke-labs | ARB, KUM, KOT, SIN, WEB, SAY, SQU, PAL, UTI, etc. | (default) |
| spottedinprod | SIP | `--workspace spottedinprod` |

---

## issue queries

### list all issues for team

```bash
linear issue list --team ARB --json -q
```

### filter by state

```bash
linear issue list --team ARB --state "Todo" --json -q
linear issue list --team ARB --state "In Progress" --json -q
linear issue list --team ARB --state "Backlog" --json -q
```

### filter by assignee

```bash
linear issue list --team ARB --assignee luke --json -q
linear issue list --team ARB --assignee unassigned --json -q
```

### combined filters

```bash
linear issue list --team ARB --state "Todo" --assignee luke --limit 20 --json -q
```

### view single issue

```bash
linear issue view ARB-123 --json -q
linear issue view ARB-123 --json | jq '{id, identifier, title, state: .state.name, description}'
```

---

## comment operations

### list comments

```bash
linear comment list ARB-123 --json -q
linear comment list ARB-123 --json -q | jq -r '.[].body'
```

### check for context markers

```bash
linear comment list ARB-123 --json -q | jq -r '.[].body' | grep -c "issue-context:" || echo "0"
```

### check marker freshness

```bash
linear comment list ARB-123 --json -q | jq -r '.[] | select(.body | contains("issue-context:")) | .createdAt'
```

### create comment

```bash
linear comment create -i ARB-123 -b "comment body"
```

---

## batch operations

### get all issue identifiers

```bash
linear issue list --team ARB --json -q | jq -r '.[].identifier'
```

### count issues by state

```bash
linear issue list --team ARB --json -q | jq 'group_by(.state.name) | map({state: .[0].state.name, count: length})'
```

### count issues by priority

```bash
linear issue list --team ARB --json -q | jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'
```

### find issues without description

```bash
linear issue list --team ARB --json -q | jq '[.[] | select(.description == null or .description == "")] | .[].identifier'
```

### find high priority issues

```bash
linear issue list --team ARB --json -q | jq '[.[] | select(.priority <= 2)] | .[].identifier'
```

---

## context checking patterns

### check single issue for context

```bash
ISSUE="ARB-123"
MARKERS=$(linear comment list $ISSUE --json -q 2>/dev/null | jq -r '.[].body' | grep -c "issue-context:" || echo "0")
if [ "$MARKERS" -gt 0 ]; then
  echo "$ISSUE: has context"
else
  echo "$ISSUE: no context"
fi
```

### batch check for context

```bash
TEAM="ARB"
linear issue list --team $TEAM --limit 50 --json -q | jq -r '.[].identifier' | while read ISSUE; do
  MARKERS=$(linear comment list $ISSUE --json -q 2>/dev/null | jq -r '.[].body' | grep -c "issue-context:" || echo "0")
  echo "$ISSUE: $MARKERS"
done
```

### check context freshness

```bash
ISSUE="ARB-123"
CONTEXT_DATE=$(linear comment list $ISSUE --json -q | jq -r '.[] | select(.body | contains("issue-context:analysis")) | .createdAt' | head -1)
if [ -n "$CONTEXT_DATE" ]; then
  DAYS_AGO=$(( ($(date +%s) - $(date -j -f "%Y-%m-%dT%H:%M:%S" "${CONTEXT_DATE%.*}" +%s)) / 86400 ))
  echo "$ISSUE: context is $DAYS_AGO days old"
fi
```

---

## state distribution query

```bash
linear issue list --team ARB --json -q | jq '
  group_by(.state.name) |
  map({
    state: .[0].state.name,
    count: length,
    issues: [.[].identifier]
  }) |
  sort_by(-.count)
'
```

output:
```json
[
  { "state": "Done", "count": 25, "issues": ["ARB-1", ...] },
  { "state": "Backlog", "count": 15, "issues": ["ARB-50", ...] },
  { "state": "Todo", "count": 8, "issues": ["ARB-100", ...] },
  { "state": "In Progress", "count": 3, "issues": ["ARB-120", ...] }
]
```

---

## enrichment queue generation

```bash
# Find issues needing enrichment
TEAM="ARB"

# Issues without any context markers
NO_CONTEXT=$(linear issue list --team $TEAM --limit 50 --json -q | jq -r '.[].identifier' | while read ISSUE; do
  MARKERS=$(linear comment list $ISSUE --json -q 2>/dev/null | jq -r '.[].body' | grep -c "issue-context:" || echo "0")
  if [ "$MARKERS" -eq 0 ]; then
    echo "$ISSUE"
  fi
done)

# Issues with stale context (>14 days)
# ... similar pattern with date check

# Combine into enrichment queue
echo "$NO_CONTEXT" | sort -u > /tmp/enrichment-queue.txt
```

---

## team mapping

```bash
# Map team key to project path
get_project_path() {
  case $1 in
    ARB) echo ~/Developer/arbor/arbor-xyz ;;
    KUM) echo ~/Developer/kumori/kumori-xyz ;;
    KOT) echo ~/Developer/koto/koto-xyz ;;
    SIN) echo ~/Developer/sine/sine-xyz ;;
    WEB) echo ~/Developer/webs/webs-xyz ;;
    SAY) echo ~/Developer/saya/saya-xyz ;;
    SQU) echo ~/Developer/squish/squish-xyz ;;
    PAL) echo ~/Developer/pal/pal-xyz ;;
    UTI) echo ~/Developer/utils ;;
    SIP) echo ~/Developer/spottedinprod/sip ;;
    *) echo "unknown" ;;
  esac
}

# Map path to team key
get_team_from_path() {
  case $1 in
    */arbor/*) echo "ARB" ;;
    */kumori/*) echo "KUM" ;;
    */koto/*) echo "KOT" ;;
    */sine/*) echo "SIN" ;;
    */webs/*) echo "WEB" ;;
    */saya/*) echo "SAY" ;;
    */squish/*) echo "SQU" ;;
    */pal/*) echo "PAL" ;;
    */utils*) echo "UTI" ;;
    */spottedinprod/*) echo "SIP" ;;
    *) echo "unknown" ;;
  esac
}
```

---

## json field extraction

### common fields

```bash
# Get all fields
linear issue view ARB-123 --json | jq 'keys'

# Common extractions
linear issue view ARB-123 --json | jq '{
  id,
  identifier,
  title,
  description,
  state: .state.name,
  priority,
  assignee: .assignee.name,
  labels: [.labels[].name],
  createdAt,
  updatedAt
}'
```

### extract for audit

```bash
linear issue list --team ARB --json -q | jq '[.[] | {
  identifier,
  title,
  state: .state.name,
  priority,
  has_description: (.description != null and .description != ""),
  label_count: (.labels | length)
}]'
```

---

## error handling

```bash
# Handle missing issue
if ! linear issue view ARB-999 --json -q 2>/dev/null; then
  echo "Issue ARB-999 not found"
fi

# Handle empty result
ISSUES=$(linear issue list --team ARB --state "Todo" --json -q)
if [ "$(echo "$ISSUES" | jq 'length')" -eq 0 ]; then
  echo "No todo issues found"
fi

# Handle rate limiting
# Linear CLI doesn't have explicit rate limit errors, but batch cautiously
# Use --limit and pagination for large queries
```

---

## integration with issue-context

```bash
# After linear-audit identifies enrichment queue
while read ISSUE; do
  echo "Enriching $ISSUE..."

  # issue-context skill handles:
  # 1. Parse issue details
  # 2. Gather codebase context
  # 3. Generate analysis comment
  # 4. Generate agent prompt comment
  # 5. Post to Linear

  # Rate limit: 3 enrichments at a time
  sleep 2
done < /tmp/enrichment-queue.txt
```

# CLI Integration for Linear Audit

Command patterns for tools used in linear-audit workflow.

---

## Linear CLI

### Authentication

Linear CLI requires workspace flag for Luke's setup:

```bash
# Always use --workspace flag
linear issue list --team ARBOR --workspace luke-labs
linear issue view ARBOR-123 --workspace luke-labs

# Available workspaces
linear workspace list --validate
```

### Issue Operations

```bash
# View issue (human readable)
linear issue view $ISSUE_ID --workspace luke-labs

# View issue (JSON)
linear issue view $ISSUE_ID --json --workspace luke-labs

# List issues with filters
linear issue list --team $TEAM --workspace luke-labs
linear issue list --team $TEAM --state "$STATE" --workspace luke-labs
linear issue list --team $TEAM --state "$STATE" --assignee $USER --json --workspace luke-labs

# Search issues
linear issue search --query "$QUERY" --limit 10 --json --workspace luke-labs

# Edit issue state
linear issue edit $ISSUE_ID --state "In Progress" --workspace luke-labs
linear issue edit $ISSUE_ID --state "Done" --workspace luke-labs
linear issue edit $ISSUE_ID --state "Canceled" --workspace luke-labs
```

### Comment Operations

```bash
# Create comment (NOTE: -i for issue ID)
linear comment create -i $ISSUE_ID -b "$BODY" --workspace luke-labs

# List comments (NOTE: positional argument)
linear comment list $ISSUE_ID --workspace luke-labs
linear comment list $ISSUE_ID --json --workspace luke-labs

# Find existing issue-context comments
linear comment list $ISSUE_ID --json --workspace luke-labs | jq -r '.[].body' | rg "issue-context:"
```

### JSON Field Extraction

```bash
# Inspect available fields
linear issue view $ISSUE_ID --json --workspace luke-labs | jq 'keys'

# Extract key fields
linear issue view $ISSUE_ID --json --workspace luke-labs | jq '{identifier, title, state: .state.name}'
linear issue view $ISSUE_ID --json --workspace luke-labs | jq '{labels: [.labels[].name], assignee: .assignee.name}'

# Group by state
linear issue list --team $TEAM --json --workspace luke-labs | jq 'group_by(.state.name) | map({state: .[0].state.name, count: length})'
```

### URL Construction

```bash
# Workspace slug != team prefix
# luke-labs workspace → ARBOR/KUMORI/etc teams
# spottedinprod workspace → SPOTS team
echo "https://linear.app/luke-labs/issue/$ISSUE_ID"
```

---

## Outline CLI

AST-based codebase mapping (10-50x token savings vs reading files).

```bash
# Structure overview (pipe from fd)
fd -e ts -e tsx . src | outline -c --format=yaml

# Function/class focus
outline -c --format=yaml --types=function,class $FILES

# Call graph (mermaid)
outline --graph --format=mermaid $FILES

# Trace callers (who calls this?)
outline --callers=$FUNCTION $FILES --format=yaml

# Trace callers of callers
outline --callers=$FUNCTION $FILES --trace-depth=2 --format=yaml

# Trace callees (what does this call?)
outline --callees=$FUNCTION $FILES --format=yaml

# Find dead code
outline --unused $FILES --format=yaml

# Diff mode (structural changes)
outline --diff=HEAD~1 --format=yaml
outline --diff=main --format=yaml

# Stats dashboard
outline --stats --format=yaml
```

---

## Layer CLI

Dependency graphs and architecture visualization.

```bash
# Package deps (monorepo default)
layer . --mode=packages --format=mermaid

# File deps
layer . --mode=files --format=mermaid

# Pipe file list from fd
fd -e ts src | layer --stdin --format=mermaid

# Focused area (packages within N hops)
layer . --focus="$PACKAGE" --depth=2 --format=mermaid

# What depends on this? (upstream)
layer . --dependents="$PACKAGE" --format=mermaid

# What does this depend on? (downstream)
layer . --dependencies="$PACKAGE" --format=mermaid

# Detect cycles
layer . --check-cycles

# JSON for programmatic use
layer . --format=json --quiet | jq '.layers'
```

---

## Git CLI

Repository history and progress tracking.

```bash
# Recent commits
git log --oneline --since="4 weeks ago" --all | head -40

# By author
git log --oneline --author="name" --since="4 weeks ago"

# By keyword in message
git log --oneline --grep="keyword" --since="4 weeks ago"

# Files changed in commits
git log --oneline --name-only --since="2 weeks ago" -- "path/"

# Contributors to area
git log --format="%an" --since="4 weeks ago" -- "path/" | sort | uniq -c

# Show commit details
git show --stat $HASH

# Check for related branches
git branch -a | rg -i "feature|issue|$ISSUE_ID"

# Check recent PRs
gh pr list --state all --limit 20 | rg -i "keyword"
```

---

## Verify CLI

Test runner adapter.

```bash
# Quick check
verify --format=summary

# With coverage
verify --coverage

# JSON for parsing
verify --json --failures-only

# Changed tests only
verify --changed
```

---

## Trails CLI

Audit persistence and replay.

```bash
# Start audit trace
export AGENTS_TRACE_ID=$(trails trail record --agent claude --new-trace --action started --task "linear-audit: $TEAM" --json -q | jq -r '.trace_id')

# Progress
trails trail record --agent claude --trace-id $AGENTS_TRACE_ID --action progress --task "specialists complete" --confidence 7

# Complete with gist
trails trail record --agent claude --trace-id $AGENTS_TRACE_ID --action completed --task "$TEAM: $READY ready, $GAPS gaps" --confidence 9 --gist

# Replay for Slack
trails trail replay --trace-id $AGENTS_TRACE_ID --format slack | slack agent post -a claude -c agents -w saya
```

---

## Combined Patterns

```bash
# Pipe outline to layer for dependency graph
fd -e ts -e tsx . src/components | layer --stdin --format=mermaid

# Targeted mapping based on issue keywords
rg -l "$KEYWORD" --type ts | outline -c --format=yaml

# Full context gathering
cd "$PROJECT_PATH"
layer . --format=json -q > /tmp/architecture.json
outline --stats --format=yaml > /tmp/code-structure.yaml
verify --format=summary 2>/dev/null || echo "no tests"
git log --oneline -10
linear issue list --team $TEAM --json --workspace luke-labs > /tmp/issues.json
```

---

## Team Mapping (Linear)

| Linear Team | Short Key | Project | Path | Type |
|-------------|-----------|---------|------|------|
| ARBOR | ARB | arbor | ~/Developer/arbor/arbor-xyz | convex-next |
| KUMORI | KUM | kumori | ~/Developer/kumori/kumori-xyz | convex-next |
| KOTO | KOT | koto | ~/Developer/koto/koto-xyz | convex-next |
| SINE | SIN | sine | ~/Developer/sine/sine-xyz | convex-next |
| WEBS | WEB | webs | ~/Developer/webs/webs-xyz | convex-next |
| SAYA | SAY | saya | ~/Developer/saya/saya-xyz | convex-next |
| SQUISH | SQU | squish | ~/Developer/squish/squish-xyz | convex-next |
| PAL | PAL | pal | ~/Developer/pal/pal-xyz | convex-next |
| UTILS | UTI | utils | ~/Developer/utils | library |
| SPOTS | SIP | spottedinprod | ~/Developer/spottedinprod/sip | convex-next |

**Note**: Use full team name (ARBOR not ARB) with linear CLI.

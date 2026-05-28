# CLI Patterns for Issue Context

Command reference for the tools used in issue context enrichment.

## outline

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

# Include imports (depth=1 for direct imports)
outline -c --format=yaml --depth=1 $FILE

# Text format for quick scanning
outline -c --format=text $FILES
```

## layer

Dependency graphs and architecture visualization.

```bash
# Package deps (monorepo default)
layer . --mode=packages --format=mermaid

# File deps
layer . --mode=files --format=mermaid

# Pipe file list from fd/find
fd -e ts src | layer --stdin --format=mermaid

# Focused area (packages within N hops)
layer . --focus="$PACKAGE" --depth=2 --format=mermaid

# What depends on this? (upstream)
layer . --dependents="$PACKAGE" --format=mermaid

# What does this depend on? (downstream)
layer . --dependencies="$PACKAGE" --format=mermaid

# Detect cycles
layer . --check-cycles

# Sequence diagram
layer . --mode=files --diagram=sequence --format=mermaid

# Create gist
layer . --format=mermaid --gist --gist-description="$DESC"

# Export to file
layer . --format=mermaid -o diagram.md

# JSON for programmatic use
layer . --format=json --quiet | jq '.layers'
```

## linear

Issue management and commenting.

```bash
# View issue (human readable)
linear issue view $ISSUE_ID

# View issue (JSON)
linear issue view $ISSUE_ID --json

# List issues with filters
linear issue list --team $TEAM --state "$STATE" --assignee $USER --json

# Search issues
linear issue search --query "$QUERY" --limit 10 --json

# Create comment (NOTE: -i for issue ID)
linear comment create -i $ISSUE_ID -b "$BODY"

# List comments (NOTE: positional argument)
linear comment list $ISSUE_ID
linear comment list $ISSUE_ID --json

# Extract key fields (inspect keys first)
linear issue view $ISSUE_ID --json | jq 'keys'
linear issue view $ISSUE_ID --json | jq '{identifier, title, state: .state.name}'
linear issue view $ISSUE_ID --json | jq '{labels: [.labels[].name], assignee: .assignee.name}'

# Find existing issue-context comments
linear comment list $ISSUE_ID --json | jq -r '.[].body' | rg "issue-context:"
```

**URL Construction**:
```bash
# Workspace slug != team prefix!
# luke-labs -> ARB/KUM/etc, spottedinprod -> SIP
echo "https://linear.app/$WORKSPACE_SLUG/issue/$ISSUE_ID"
```

## git

Repository history and progress tracking.

```bash
# Recent commits
git log --oneline --since="4 weeks ago" --all | head -40

# By author
git log --oneline --author="name" --since="4 weeks ago"

# By keyword in message
git log --oneline --grep="keyword" --since="4 weeks ago"

# Grep through commit messages with rg
git log --oneline --all | rg -i "pattern"

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

## Combined Patterns

```bash
# Pipe outline to layer for dependency graph
fd -e ts -e tsx . src/components | layer --stdin --format=mermaid

# Targeted mapping based on issue keywords
rg -l "$KEYWORD" --type ts | outline -c --format=yaml

# For multi-repo (e.g., sip + sip-api pattern)
for repo in sip sip-api; do
  echo "=== $repo ==="
  fd -e ts -e tsx . "../$repo/src" 2>/dev/null | outline -c --format=yaml | head -50
done
```

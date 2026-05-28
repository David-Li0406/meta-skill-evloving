# Common Workflows

## Workflow 1: Understanding a New Codebase

**Goal**: Get oriented in an unfamiliar project

```bash
# Step 1: Run analysis
llm-context analyze

# Step 2: Read system overview
cat .llm-context/summaries/L0-system.md

# Step 3: Get statistics
llm-context stats

# Step 4: Find entry points
llm-context entry-points

# Step 5: Explore a specific domain
cat .llm-context/summaries/L1-domains.json | jq '.[] | select(.domain == "src/auth")'
```

**LLM Response Template:**
```
Based on the analysis:

Architecture: [from L0]
- X functions across Y files
- Key domains: [list from L1]
- Entry points: [list]

The codebase is organized as:
[domain breakdown]

Would you like me to explain a specific module?
```

---

## Workflow 2: Daily Development

**Goal**: Keep analysis fresh as you code

```bash
# Morning: Pull latest
git pull origin main

# Check what changed
llm-context check-changes

# Re-analyze (auto-incremental)
llm-context analyze

# Work on feature...
vim src/feature.js

# Quick re-analysis after edits
llm-context analyze  # Only analyzes feature.js
```

**Time Savings:**
- Full analysis: 4.2s
- Incremental: 127ms
- **97% faster**

---

## Workflow 3: Debugging

**Goal**: Understand why a function is failing

```bash
# Step 1: Find the function
llm-context query find-function buggyFunction

# Step 2: See what calls it
llm-context query calls-to buggyFunction

# Step 3: See what it calls
llm-context query called-by buggyFunction

# Step 4: Trace full call path
llm-context query trace buggyFunction

# Step 5: Check for side effects
llm-context side-effects | grep buggy
```

**LLM Analysis:**
```
The buggyFunction call path:
- Called by: handleRequest, processData
- Calls: validateInput, db.query, sendEmail
- Side effects: database, network

Potential issues:
1. Database query without error handling
2. Network call (sendEmail) could timeout
3. No input validation shown in calls

[Read specific file to investigate]
```

---

## Workflow 4: Code Review

**Goal**: Review PR changes systematically

```bash
# Checkout PR branch
git checkout feature/new-auth

# Re-analyze
llm-context analyze

# Compare before/after
llm-context stats

# Find new entry points
llm-context entry-points

# Check for new side effects
llm-context side-effects | grep -A2 "auth"

# Trace critical paths
llm-context query trace authenticateUser
```

**Review Checklist:**
- [ ] New entry points documented?
- [ ] Side effects properly handled?
- [ ] Call graph doesn't introduce cycles?
- [ ] Functions follow naming conventions?

---

## Workflow 5: Refactoring

**Goal**: Safely rename/restructure code

```bash
# Before refactoring: Document current state
llm-context analyze
llm-context query calls-to oldFunctionName > before.txt

# Perform refactor...
# (rename oldFunctionName → newFunctionName)

# After refactoring: Verify
llm-context analyze
llm-context query calls-to newFunctionName > after.txt

# Compare impact
diff before.txt after.txt
```

**Safety Checks:**
- All callers updated?
- No broken references?
- Side effects preserved?

---

## Workflow 6: Architecture Review

**Goal**: Evaluate codebase structure

```bash
# Get overview
llm-context stats

# Review domain organization
cat .llm-context/summaries/L1-domains.json | jq

# Check module sizes
cat .llm-context/summaries/L2-modules.json | jq '.[] | {module, functionCount}'

# Find highly coupled modules
cat .llm-context/graph.jsonl | jq -r '.calls[]' | sort | uniq -c | sort -rn | head
```

**Red Flags:**
- Modules > 50 functions
- High coupling between domains
- Too many entry points (> 20)
- Side effects not grouped by domain

---

## Workflow 7: Onboarding New Team Member

**Goal**: Help new developer understand codebase

```bash
# Generate fresh analysis
llm-context analyze:full

# Create onboarding doc
cat > ONBOARDING.md <<EOF
# Codebase Overview

$(cat .llm-context/summaries/L0-system.md)

## Quick Stats
$(llm-context stats)

## Start Here
$(llm-context entry-points | head -10)

## Common Queries
- Find function: llm-context query find-function NAME
- Trace calls: llm-context query trace NAME
EOF
```

---

## Workflow 8: Performance Investigation

**Goal**: Find performance bottlenecks

```bash
# Find functions with file I/O
llm-context side-effects | grep file_io

# Find functions with network calls
llm-context side-effects | grep network

# Trace from slow entry point
llm-context query trace slowEndpoint

# Check for long call chains
cat .llm-context/graph.jsonl | jq 'select(.calls | length > 10)'
```

**Look for:**
- Sync file operations in hot paths
- Network calls without caching
- Deep call chains (> 10 levels)
- Database queries in loops

---

## Workflow 9: CI/CD Integration

**Goal**: Auto-analyze on every commit

```yaml
# .github/workflows/analyze.yml
name: Code Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install llm-context
        run: npm install -g llm-context

      - name: Run analysis
        run: llm-context analyze

      - name: Check for breaking changes
        run: |
          # Compare entry points
          llm-context entry-points > current.txt
          git checkout main
          llm-context entry-points > previous.txt
          diff previous.txt current.txt || echo "Entry points changed!"

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: llm-context
          path: .llm-context/
```

---

## Workflow 10: Pre-commit Hook

**Goal**: Keep analysis always up-to-date

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Analyzing codebase..."
llm-context analyze

# Add analysis to commit
git add .llm-context/graph.jsonl
git add .llm-context/manifest.json
git add .llm-context/summaries/

echo "✓ Analysis updated"
```

**Benefits:**
- Always current context
- Reviewers can query the PR's state
- Track architectural changes over time

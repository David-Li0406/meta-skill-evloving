---
name: epic-scout
description: Scan existing epics to find dependencies and relationships for a new plan. Use when planning a new feature to identify if it depends on or conflicts with existing work.
---

# Epic Scout

Epic dependency scout to find relationships between a new plan and existing epics.

**Role**: Dependency finder
**Purpose**: Find relationships between new plans and existing epics
**Speed**: Fast - check titles/scope first, only read specs if relevant

## Tool Requirements

**Required tools**: Read, Glob

**Degradation strategy** (if tools unavailable):
```
File tools not available. Please check manually:

1. List epics:
   .flow/bin/flowctl epics --json

2. View epic spec:
   .flow/bin/flowctl cat <epic-id>

3. List tasks for epic:
   .flow/bin/flowctl tasks --epic <epic-id> --json
```

## Input

You receive:
- `REQUEST` - the feature/change being planned
- `FLOWCTL` - path to flowctl CLI

## Process

### 1. List open epics

```bash
$FLOWCTL epics --json
```

Filter to `status: "open"` epics only. Skip done epics.

### 2. For each open epic, read its spec

```bash
$FLOWCTL cat <epic-id>
```

Extract:
- Title and scope
- Key files/paths mentioned
- APIs, functions, data structures defined
- Acceptance criteria

### 3. Find relationships

Compare the new REQUEST against each epic's scope. Look for:

**Dependency signals** (new plan depends on epic):
- New plan needs APIs/functions the epic is building
- New plan touches files the epic owns
- New plan extends data structures the epic creates
- Explicit mentions ("after X is done", "requires Y")

**Reverse dependency signals** (epic depends on new plan):
- Epic mentions needing something the new plan provides
- Epic blocked waiting for infrastructure the new plan adds

**Overlap signals** (potential conflict, not dependency):
- Both touch same files
- Both modify same data structures
- Risk of merge conflicts

### 4. Check task-level overlap

For epics with potential relationships:

```bash
$FLOWCTL tasks --epic <epic-id> --json
```

Look at in_progress and todo tasks for specific overlaps.

## Output Format

```markdown
## Epic Dependencies

### Dependencies (new plan depends on these)
- **fn-2-abc** (Auth system): New plan uses `authService` from fn-2-abc.1
- **fn-5-xyz** (DB schema): New plan extends `User` model defined in fn-5-xyz.3

### Reverse Dependencies (these may depend on new plan)
- **fn-7-def** (Notifications): Waiting for event system this plan adds

### Overlaps (potential conflicts, not dependencies)
- **fn-3-ghi** (Refactor): Both touch `src/api/handlers.ts`

### No Relationship
- fn-4-jkl, fn-6-mno, fn-8-pqr: Unrelated scope
```

If no relationships found:
```markdown
## Epic Dependencies

No dependencies or overlaps detected with open epics.
```

## Rules

- Speed over completeness - check titles/scope first, only read specs if relevant
- Only report clear relationships, not maybes
- Skip done epics entirely
- Keep analysis fast
- Return structured output for planner to auto-set deps

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo"
  exit 1
fi

ls "$REPO_ROOT/.factory/skills/epic-scout/SKILL.md"
# Expected: file exists, exit code 0

# Verify flowctl is callable
"$REPO_ROOT/.flow/bin/flowctl" --help >/dev/null 2>&1 && echo "flowctl OK"
# Expected: outputs "flowctl OK", exit code 0
````

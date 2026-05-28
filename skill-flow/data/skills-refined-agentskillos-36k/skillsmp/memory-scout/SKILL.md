---
name: memory-scout
description: Search project memory (.flow/memory/) for entries relevant to the current task or request. Use when you need to recall past pitfalls, conventions, or decisions that apply to the work at hand.
---

# Memory Scout

Memory scout to search `.flow/memory/` for entries relevant to the current context.

**Role**: Memory searcher
**Purpose**: Find relevant past lessons, conventions, and decisions
**Speed**: Fast - simple keyword/semantic matching

## Tool Requirements

**Required tools**: Read, Glob

**Degradation strategy** (if tools unavailable):
```
File tools not available. Please check manually:

1. View memory files:
   ls .flow/memory/
   cat .flow/memory/pitfalls.md
   cat .flow/memory/conventions.md
   cat .flow/memory/decisions.md

2. Search for keywords:
   grep -i "<keyword>" .flow/memory/*.md
```

## Input

You receive either:
- A planning request (feature description, change request)
- A task identifier with title (e.g., "fn-1-abc.3: flowctl memory commands")

## Memory Location

Files live in `.flow/memory/`:
- `pitfalls.md` - Lessons from NEEDS_WORK reviews (what models miss)
- `conventions.md` - Project patterns not in CLAUDE.md
- `decisions.md` - Architectural choices with rationale

## Search Strategy

1. **Read all memory files** using Read tool
2. **Find semantically related entries** based on input context
3. **Return ONLY relevant entries** (not everything)

### Relevance Criteria
- Same technology/framework mentioned
- Similar type of work (API, UI, config, etc.)
- Related patterns or conventions
- Applicable pitfalls or gotchas

## Output Format

```markdown
## Relevant Memory

### Pitfalls
- [Issue] - [Fix] (from <task-id>)

### Conventions
- [Pattern] (discovered <date>)

### Decisions
- [Choice] because [rationale]
```

If no relevant entries found:
```markdown
## Relevant Memory

No relevant entries in project memory.
```

## Rules

- Speed is critical - simple keyword/semantic matching
- Return ONLY relevant entries (max 5-10 items)
- Preserve entry context (dates, task IDs)
- Handle empty memory gracefully
- Handle missing files gracefully
- Never return entire memory contents

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo"
  exit 1
fi

ls "$REPO_ROOT/.factory/skills/memory-scout/SKILL.md"
# Expected: file exists, exit code 0

# Check memory directory exists
ls "$REPO_ROOT/.flow/memory/" 2>/dev/null || echo "Memory directory not found (may not exist yet)"
````

---
name: knowledge
description: 'Query knowledge artifacts across all locations. Triggers: "find learnings", "search patterns", "query knowledge", "what do we know about", "where is the plan".'
---

# Knowledge Skill

Query and retrieve knowledge from artifacts across the codebase.

## Quick Start

```bash
/knowledge patterns authentication
/knowledge learnings kubernetes
/knowledge "what do we know about rate limiting"
```

## Knowledge Locations

| Type | Location | Format |
|------|----------|--------|
| Learnings | `.agents/learnings/` | JSONL or Markdown |
| Patterns | `.agents/patterns/` | Markdown |
| Retros | `.agents/retros/` | Markdown |
| Research | `.agents/research/` | Markdown |
| Plans | `~/.claude/plans/` | Markdown |

## Query Methods

### 1. Semantic Search (via ao CLI)

```bash
ao forge search "<query>"
```

### 2. File Pattern Search

```bash
# Find learnings about a topic
grep -r "<topic>" .agents/learnings/ .agents/patterns/

# Find plans for current project
grep -l "$(pwd)" ~/.claude/plans/*.md
```

### 3. JSONL Queries

```bash
# Query learnings JSONL
jq -r 'select(.tags[] | contains("<topic>"))' .agents/learnings/*.jsonl

# Count by category
jq -r '.category' .agents/learnings/*.jsonl | sort | uniq -c
```

## Artifact Format

### Learnings (JSONL)

```json
{
  "id": "L-001",
  "date": "2026-01-25",
  "category": "kubernetes",
  "learning": "DeepCopy required for CRD mutations",
  "context": "Epic he-xyz",
  "tags": ["kubernetes", "crd", "deepcopy"]
}
```

### Patterns (Markdown)

```markdown
# Pattern: Wave-Based Parallel Execution

## Problem
Sequential execution too slow for large epics

## Solution
Group issues by dependencies, execute in parallel waves

## When to Use
- Epics with 5+ issues
- Issues without circular dependencies
```

## Workflow

1. **Parse query** - Extract topic and scope
2. **Search locations** - Check all artifact directories
3. **Rank results** - By relevance and recency
4. **Synthesize** - Combine and summarize findings
5. **Output** - Return formatted results

## Integration with ao CLI

When ao CLI is available:

```bash
# Search indexed knowledge
ao forge search "<query>" --limit 10

# Get provenance chain
ao ratchet provenance <artifact-id>

# Record new knowledge
ao ratchet record --type learning --content "<content>"
```

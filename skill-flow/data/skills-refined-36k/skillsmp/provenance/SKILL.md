---
name: provenance
description: 'Trace knowledge artifact lineage and sources. Find orphans, stale citations. Triggers: "where did this come from", "trace this learning", "knowledge lineage".'
---

# Skill: Provenance

> Trace knowledge lineage. Every insight has a source.

## Triggers

- `/provenance <artifact>`
- "where did this come from"
- "trace this learning"
- "show source for"
- "knowledge lineage"

## Synopsis

```bash
/provenance <path>              # Trace single artifact
/provenance --orphans           # Find knowledge without sources
/provenance --stale             # Find outdated citations
/provenance --graph <artifact>  # Show citation graph
```

## What It Does

1. **Parse** - Read artifact's metadata
2. **Resolve** - Find source transcript(s)
3. **Trace** - Build lineage chain
4. **Report** - Show provenance with context

## Lineage Chain

```
Transcript (source of truth)
    ↓
Forge extraction (candidate)
    ↓
Human review (promotion)
    ↓
Pattern recognition (tier-up)
    ↓
Skill creation (automation)
```

## Output

```markdown
# Provenance: always-push-before-done.md

## Current State
- **Tier:** 1 (Learning)
- **Created:** 2026-01-15
- **Citations:** 4

## Source Chain
1. **Origin:** transcript-xyz789.jsonl
   - Line: 2341-2367
   - Context: "Session ended without pushing, lost 2 hours of work"
   - Extracted: 2026-01-15T14:23:00Z

2. **Promoted:** Tier 0 → Tier 1
   - Reason: 2 citations within 7 days
   - Promoted: 2026-01-17T09:00:00Z

## Citations
- transcript-abc123.jsonl:891 (2026-01-16)
- transcript-def456.jsonl:1234 (2026-01-17)
- transcript-ghi789.jsonl:567 (2026-01-20)
- transcript-jkl012.jsonl:2341 (2026-01-23)

## Related
- patterns/session-discipline.md (Tier 2)
- skills/commit/SKILL.md (references this)
```

## Orphan Detection

```bash
/provenance --orphans

# Output:
# Found 3 orphaned artifacts (no source transcript):
# - .agents/learnings/legacy-pattern.md
# - .agents/patterns/old-approach.md
# - .agents/decisions/undocumented.md
```

## Staleness Check

```bash
/provenance --stale

# Output:
# Found 2 stale artifacts (source modified since extraction):
# - .agents/learnings/api-design.md
#   Source changed: 2026-01-22 (artifact: 2026-01-10)
```

## Metadata Format

Each forged artifact includes:

```yaml

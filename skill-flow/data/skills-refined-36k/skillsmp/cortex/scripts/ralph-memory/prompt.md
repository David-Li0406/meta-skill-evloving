# Ralph Agent Instructions — Cortex Memory System

## Context

You are implementing the **Cortex Memory System** — a Graphiti-inspired knowledge graph for personal memory. This adds:

- **Entity extraction and resolution** — People, Companies, Projects, Locations, Events, Documents, Pets
- **Relationship extraction** — Facts as triples with temporal bounds
- **Identity promotion** — Emails/phones → aliases (not entities)
- **Contradiction detection** — Invalidate stale facts
- **Merge system** — Deduplicate entities with human review

The detailed specification is in `docs/MEMORY_SYSTEM_SPEC.md` — **READ THE RELEVANT SECTIONS**.

## Key Files

- `docs/MEMORY_SYSTEM_SPEC.md` — **The full specification** (READ RELEVANT PARTS)
- `prompts/graphiti/README.md` — Prompt overview and entity/relationship types
- `prompts/graphiti/extract-entities.prompt.md` — Entity extraction prompt
- `prompts/graphiti/extract-relationships.prompt.md` — Relationship extraction prompt
- `scripts/ralph-memory/prd.json` — User stories with acceptance criteria
- `scripts/ralph-memory/progress.txt` — Learnings and patterns
- `AGENTS.md` — Codebase patterns for Cortex

## Your Task

1. Read `scripts/ralph-memory/prd.json` for user stories
2. Read `scripts/ralph-memory/progress.txt` (especially Codebase Patterns at top)
3. Pick the highest priority story where `passes: false`
4. Read the relevant section of `docs/MEMORY_SYSTEM_SPEC.md` for that story
5. Implement that ONE story following the spec
6. Run `go build ./cmd/cortex` to verify it compiles
7. Run `go test ./...` if tests exist
8. Update AGENTS.md with learnings about this codebase
9. Commit: `feat(memory): [MS-XXX] - [Title]`
10. Update prd.json: set `passes: true` for completed story
11. Append learnings to progress.txt

## Key Spec Sections by Story

| Story | Spec Section |
|-------|--------------|
| MS-001 | Part 1: Naming Changes |
| MS-002 to MS-008 | Part 3.4: SQLite Schema Additions |
| MS-009 | Part 3.2: Entity Types |
| MS-010 | Part 4.1 step 1, prompts/graphiti/extract-entities.prompt.md |
| MS-011 | Part 4.1 step 7 |
| MS-012 | Part 4.2: Entity Resolution Details |
| MS-013 | Part 4.1 step 3, prompts/graphiti/extract-relationships.prompt.md |
| MS-014 | Part 4.4: Identity Promotion |
| MS-015 | Part 4.1 step 4 |
| MS-016 | Part 4.1 step 6, Part 10.9 |
| MS-017 | Part 8.4: Collision Detection Algorithm |
| MS-018 | Part 8.5-8.7: Conflict Detection, Auto-Merge, Execution |
| MS-019 | Part 4.1: Pipeline Overview |
| MS-020 | Part 10.12: Query Layer Tests |
| MS-021-022 | Part 11: Verification Harness |

## Critical Design Decisions

1. **8 Entity Types**: Person, Company, Project, Location, Event, Document, Pet, Entity (fallback)
2. **NO Date entities** — dates are `target_literal` on temporal relationships (ISO 8601)
3. **NO Agent entities** — AI assistants have no durable identity
4. **target_literal vs target_entity_id**:
   - Identity (HAS_EMAIL, HAS_PHONE, HAS_HANDLE) → `target_literal` → promoted to aliases
   - Temporal (BORN_ON, STARTED_ON, ANNIVERSARY_ON) → `target_literal` (ISO 8601 date)
   - Everything else → `target_entity_id` (UUID reference)
5. **Graph-independent extraction** — prompts don't query the graph; resolution uses graph context
6. **Conservative merging** — prefer duplicates over false merges; use merge_candidates for review
7. **Bi-temporal model** — `valid_at`/`invalid_at` for real-world time, `created_at` for system time

## Progress Format

APPEND to progress.txt after each story:

```markdown
---
## [Date] - [MS-XXX] [Title]
- What was implemented
- Files changed
- **Learnings:**
  - Patterns discovered
  - Gotchas encountered
```

Add reusable patterns to TOP of progress.txt in Codebase Patterns section.

## Stop Condition

If ALL stories in prd.json have `passes: true`, reply:
```
<promise>COMPLETE</promise>
```

Otherwise, end normally after completing one story.

## Critical Rules

1. **ONE story per iteration** — Do not implement multiple stories
2. **Build must pass** — `go build ./cmd/cortex` must succeed before committing
3. **Follow the spec** — Use exact schema/types from MEMORY_SYSTEM_SPEC.md
4. **No placeholders** — Full implementations only
5. **Update progress.txt** — Capture learnings for future iterations
6. **Update AGENTS.md** — Document codebase patterns
7. **Commit message format** — `feat(memory): [MS-XXX] - [Title]`
8. **Test your changes** — Run tests, verify manually if needed

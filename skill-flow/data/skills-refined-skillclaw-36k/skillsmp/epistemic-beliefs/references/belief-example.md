# Belief File Format Example

This is a complete example of an epistemic belief file.

## Complete Example: sync-first

```markdown
---
type: belief
id: sync-first
persona: architect
facets: [rust, architecture, simplicity]
confidence:
  score: 0.88
  signals:
    evidence: 0.92
    source_reliability: 0.90
    recency: 0.75
    survival: 0.95
    user_endorsement: 0.85
entrenchment: high
status: active
extracted: 2025-08-04
revised: 2026-01-16
---

# sync-first

Prefer synchronous, blocking code over async in Patina.

## Statement

Use synchronous, blocking code by default. Async adds complexity (infects codebase with 'static lifetimes, complicates borrow checker) without benefit when the workload is inherently synchronous (local file I/O, SQLite queries).

## Evidence

- [[session-20250804-073015]] - "Patina's workload is inherently synchronous" (weight: 0.95)
- [[session-20250804-073015]] - "Async infects codebase with 'static lifetimes" (weight: 0.90)
- [[session-20250730-065949]] - "Chose blocking reqwest client for simplicity" (weight: 0.80)

## Supports

- [[simple-error-handling]]
- [[local-first]]
- [[dependable-rust]] - borrow checker works better without async

## Attacks

- [[async-by-default]] (status: defeated, reason: consider actual I/O patterns first)
- [[rqlite-architecture]] (status: defeated, reason: migrated to SQLite)

## Attacked-By

- [[high-concurrency-needed]] (status: active, confidence: 0.3, scope: "network-heavy scenarios")
- [[streaming-responses]] (status: active, confidence: 0.25, scope: "long-running streaming APIs")

## Applied-In

- reqwest blocking client instead of async
- rusqlite instead of async SQLite wrappers
- Standard threads for background work, not tokio tasks

## Revision Log

- 2025-08-04: Decided during SQLite migration (confidence: 0.80)
- 2025-08-04: Removed async entirely from codebase (confidence: 0.80 → 0.85)
- 2026-01-16: Added to epistemic layer, high survival (confidence: 0.85 → 0.88)
```

## Field Reference

### Required Frontmatter

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `belief` |
| `id` | string | Lowercase, hyphenated identifier |
| `persona` | string | Epistemic agent (usually `architect`) |
| `confidence.score` | float | Overall confidence 0.0-1.0 |
| `status` | enum | `active`, `scoped`, `defeated`, `archived` |
| `extracted` | date | When belief was first captured |

### Optional Frontmatter

| Field | Type | Description |
|-------|------|-------------|
| `facets` | array | Domain tags for categorization |
| `confidence.signals` | object | Individual signal scores |
| `entrenchment` | enum | `low`, `medium`, `high`, `very-high` |
| `revised` | date | Last revision date |

### Required Sections

| Section | Purpose |
|---------|---------|
| `# {id}` | Title matching the id |
| `## Statement` | Full explanation of the belief |
| `## Evidence` | Sources with wikilinks and weights |

### Optional Sections

| Section | Purpose |
|---------|---------|
| `## Supports` | Beliefs this belief supports |
| `## Attacks` | Beliefs this belief defeats |
| `## Attacked-By` | Beliefs that challenge this one |
| `## Applied-In` | Concrete applications |
| `## Context` | Additional background |
| `## Revision Log` | History of changes |

## Wikilink Conventions

- Evidence: `[[session-YYYYMMDD-HHMMSS]]` or `[[commit-sha]]`
- Beliefs: `[[belief-id]]`
- Attacks include status and reason: `(status: defeated, reason: "...")`
- Attacked-By includes confidence and scope: `(status: active, confidence: 0.3, scope: "...")`

## Confidence Guidelines

| Range | Meaning | When to Use |
|-------|---------|-------------|
| 0.90+ | Very high | Multiple sources, long survival, user endorsed |
| 0.80-0.90 | High | Strong evidence, proven in practice |
| 0.65-0.80 | Medium | Single source, recently created |
| 0.50-0.65 | Low | Inferred, needs validation |
| <0.50 | Very low | Speculative, conflicting evidence |

## Entrenchment Guidelines

| Level | Meaning | Criteria |
|-------|---------|----------|
| `very-high` | Core principle | Many dependents, foundational |
| `high` | Established | Proven over time, referenced often |
| `medium` | Working | In use, not yet proven |
| `low` | Tentative | New, experimental |

# Retro Output Templates

Document templates for retro, learnings, and patterns.

---

## Tag Vocabulary Reference

See `.claude/includes/tag-vocabulary.md` for the complete tag vocabulary.

**Document type tags:** `retro`, `learning`, `pattern`

**Examples:**
- `[retro, agents, mcp]` - MCP server implementation retro
- `[learning, data, neo4j]` - GraphRAG implementation learning
- `[pattern, testing, python]` - Python testing pattern

---

## Retro Summary Template

Write to `.agents/retros/YYYY-MM-DD-{topic}.md`:

```markdown
---
date: YYYY-MM-DD
type: Learning
topic: "[Topic]"
tags: [retro, domain-tag, optional-tech-tag]
status: COMPLETE
---

# Retrospective: [Topic]

**Date:** YYYY-MM-DD
**Epic:** [beads epic ID if applicable]
**Duration:** [Single session | Multi-session | Sprint]

---

## What We Accomplished

[Summary of work completed with commits, issues closed, metrics]

| Commit | Issue | Description |
|--------|-------|-------------|
| `abc123` | ai-platform-xxx | Feature description |

---

## What Went Well

- [Positive outcome 1]
- [Positive outcome 2]

---

## What Could Improve

- [Area for improvement 1]
- [Area for improvement 2]

---

## Patterns Worth Repeating

[Code blocks or descriptions of reusable patterns discovered]

---

## Remaining Work

[List of open issues or next steps]

---

## Session Stats

| Metric | Value |
|--------|-------|
| Issues closed | X |
| Lines added | ~Y |

## Source Performance

[Include if analytics data available from Phase 1.5]

| Source | Tier | Value Score | Expected | Deviation |
|--------|------|-------------|----------|-----------|
| [source_type] | [tier] | [value_score] | [expected_weight] | [deviation] |

### Tier Weight Recommendations

[List any recommendations from analytics endpoint]

- **PROMOTE/DEMOTE**: '[source_type]' [over/under]performing by [%]. Consider [action].
```

**Tag Rules:** First tag MUST be `retro`. Include domain tag.

---

## Learning File Template

Write to `.agents/learnings/YYYY-MM-DD-{topic}.md`:

**Tag Rules:** 3-5 tags. First tag MUST be `learning`. At least one domain tag required.

```markdown
---
date: YYYY-MM-DD
type: Learning
topic: "[Topic]"
source: "[beads ID or plan file]"
tags: [learning, domain-tag, optional-tech-tag]
status: COMPLETE
---

# Learning: [Topic]

## Context
[What were we trying to do?]

## What We Learned

### [Learning 1]
**Type:** Technical | Process | Pattern | Gotcha

[Description]

**Evidence:** [File path, beads comment, or observation]

**Application:** [How to use this knowledge in the future]

### [Learning 2]
...

## Discovery Provenance

Track which sources led to these learnings (enables flywheel optimization).

**Purpose**: Create measurement data for the knowledge flywheel. Analytics can then measure: "Which discovery sources produce the most cited, most valuable knowledge?"

**Format**:
```markdown
| Learning | Source Type | Source Detail |
|----------|-------------|---------------|
| [Learning 1] | [type] | [detail] |
| [Learning 2] | [type] | [detail] |
```

> **Note:** Do NOT include a "Confidence" column. Confidence/relevance are query-time metrics, not storage-time. See `domain-kit/skills/standards/references/rag-formatting.md`.

**Example**:
```markdown
| Middleware pattern works well | smart-connections | "request lifecycle" query |
| Rate limit algorithm at L89 | grep | services/limits.py:89 |
| Precedent from prior work | prior-research | 2026-01-01-limits.md |
```

**Source types by tier**:
- **Tier 1**: `code-map`
- **Tier 2**: `smart-connections`, `athena-knowledge`
- **Tier 3**: `grep`, `glob`
- **Tier 4**: `read`, `lsp`
- **Tier 5**: `prior-research`, `prior-retro`, `prior-pattern`, `memory-recall`
- **Tier 6**: `web-search`, `web-fetch`

**How it feeds the flywheel**:
1. You document source_type for each learning during retro
2. Session analyzer extracts these and stores as memories with source_type field
3. `GET /memories/analytics/sources` computes value_score for each source
4. High-value sources (value_score > 0.7) get promoted in discovery tier ordering
5. Future research prioritizes high-value sources = better decisions

## Related
- Plan: [link to plan file if applicable]
- Research: [link to research file if applicable]
- Issues: [beads IDs]
```

---

## Pattern File Template

Write to `.agents/patterns/`:

**Tag Rules:** 3-5 tags. First tag MUST be `pattern`. At least one domain tag required.

```markdown
---
date: YYYY-MM-DD
type: Pattern
category: "[Category]"
tags: [pattern, domain-tag, optional-tech-tag]
status: ACTIVE
---

# Pattern: [Name]

## When to Use
[Triggering conditions]

## The Pattern
[Step-by-step or code example]

## Why It Works
[Rationale]

## Examples
[Real examples from codebase with file paths]
```

---

## Progress Output Templates

### Context Summary

```
================================================================
CONTEXT GATHERED
================================================================

Epic: ai-platform-xxxx
Title: [Epic title]
Duration: [Days from first to last commit]

Sources Analyzed:
  - Commits: 12 (abc123..def456)
  - Issues: 5 (3 closed, 2 open)
  - Files modified: 8
  - Blackboard entries: 2
  - Commands used: 14

Key Files:
  - .claude/commands/retro.md (major changes)
  - services/etl/app/main.py (new)
  - tests/test_etl.py (new)

Ready for Phase 2: Identify Improvements
================================================================
```

### Friction Analysis

```
================================================================
FRICTION ANALYSIS COMPLETE
================================================================

Friction Points Found: 5
  [HIGH] Epic-child dependency confusion (3 occurrences)
  [MEDIUM] Wave detection unclear (2 occurrences)
  [LOW] Commit message format inconsistent (1 occurrence)

Improvement Opportunities: 3
  1. Update /plan command with dependency warning
  2. Add wave auto-detection to /load-epic
  3. Document commit message format in CLAUDE.md

New Patterns Discovered: 1
  - Comment-based epic-child linking

Ready for Phase 3: Propose Changes
================================================================
```

### User Review Display

```
================================================================
IMPROVEMENT PROPOSALS
================================================================

Found 4 improvements (1 critical, 2 recommended, 1 optional)

Would you like to:
1. Review each proposal individually
2. Apply all CRITICAL and RECOMMENDED (skip OPTIONAL)
3. Apply all proposals
4. Skip improvements (proceed to retro summary only)

================================================================
```

### Changes Applied

```
================================================================
CHANGES APPLIED
================================================================

Successfully applied: 3/3 proposals

Files modified:
  * .claude/commands/plan.md
  * .claude/commands/load-epic.md
  * CLAUDE.md

Commit: abc1234

Skipped (user choice): 1
  - .agents/patterns/comment-based-linking.md

Failed: 0

================================================================
```

### Supersession Report

```
================================================================
SUPERSESSION CHECK COMPLETE
================================================================

Searched for: "[topic]"
Candidates found: 3
Superseded: 1

Supersession applied:
  * .agents/learnings/2025-11-15-old-pattern.md
    -> superseded by: .agents/learnings/2025-12-31-new-pattern.md
    -> Reason: Updated approach with better performance

Cross-references added (not superseded):
  - .agents/patterns/related-pattern.md
    -> Added to "Related" section

No action needed:
  - .agents/retros/2025-10-01-unrelated.md
    -> Different topic, no relationship

Ready for Phase 5: User Review
================================================================
```

### Final Output

```
Retro complete:
- Summary: .agents/retros/YYYY-MM-DD-topic.md
- Learnings: .agents/learnings/YYYY-MM-DD-topic.md (if applicable)
- Patterns: [updated/created files] (if applicable)

This knowledge is now persistent and available to future sessions.
```

---
name: memory
description: Capture and retain project decisions, patterns, anti-patterns, and lessons learned.
---

# Memory Skill

## What this skill does

Provides a lightweight memory system that lets agents record and retrieve project decisions, patterns, anti-patterns, and lessons in a single file (`.workflow/memories.md`).

## When to activate

Trigger this skill when **you (the agent)** need to **read or write** project memory.

### Agent autonomy rules

- **Do not wait for the user to ask** to record or maintain memory. Decide proactively.
- **Generate then filter**: At the end of significant work, always generate 1-3 candidate memories, then critically evaluate each one.
- **Be selective**: For each candidate, ask "Would this help a future agent working on this codebase?" Only add memories that pass this bar — it's okay to reject all candidates.
- **Prefer update over duplication**: If a memory already exists on the topic, update it instead of adding a new entry.
- **Prefer update over delete**: Delete only when an entry is clearly incorrect, redundant, or harmful.
- **Never store secrets**: Do not write API keys, tokens, credentials, private customer data, or logs that may contain sensitive information.

### Common activation signals

- A **non-obvious decision** was made (trade-off, constraint, convention) that future work could accidentally undo.
- A **pattern** emerged that should be repeated.
- An **anti-pattern** caused avoidable pain and should be prevented.
- A **lesson** was learned after implementing, reviewing, or debugging a change.
- You need to **recall** prior choices to avoid conflicting guidance.

## File location

All memories live in a single file: `.workflow/memories.md`

## Memory format

```markdown
# Memories

Project memories captured during development. Agents should read this file for context and add new memories when significant decisions, patterns, or lessons emerge.

---

## Use batch inserts for large datasets
Type: pattern | Date: 2025-01-15 | Tags: database, performance

Bulk operations are 10x faster than individual inserts. Always batch when inserting more than 100 rows.

---
```

### Format rules

- **Heading**: `## <descriptive title>` — use imperative or declarative statement
- **Metadata line**: `Type: <type> | Date: YYYY-MM-DD | Tags: tag1, tag2`
- **Body**: 1-3 sentences, standalone (understandable without external context)
- **Separator**: `---` between entries
- **Ordering**: Newest entries at the top (after the file header)

### Valid types

| Type | When to use |
| --- | --- |
| decision | Significant trade-offs or choices |
| pattern | Approaches that worked well |
| anti-pattern | Approaches to avoid |
| lesson | Post-change learnings |

## How to edit

- **Read**: Open `.workflow/memories.md` and scan for relevant context
- **Add**: Insert new entry at the top (after the header section), with `---` separator
- **Update**: Edit the existing entry in place
- **Delete**: Remove the entry and its separator (only when incorrect, redundant, or misleading)

## Generate-then-filter workflow

At the end of significant work:

1. **Generate candidates (Required)** — Generate 1-3 potential memories from the work just completed
2. **Critically evaluate** — For each candidate, ask: "Would this help a future agent working on this codebase?"
3. **Be selective** — Only add memories that pass the bar; it's fine to generate candidates and reject all of them
4. **Write survivors** — Add any memories that passed evaluation to `.workflow/memories.md`

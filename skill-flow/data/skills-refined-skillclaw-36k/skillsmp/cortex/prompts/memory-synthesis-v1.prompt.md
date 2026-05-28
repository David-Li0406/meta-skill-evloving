# Memory Synthesis Prompt v1

## Purpose

Synthesize raw memory facets into coherent, deduplicated memory entries. This prompt takes existing memory and new extracted facets, then produces an updated memory that:
- Deduplicates redundant entries
- Merges related information
- Generalizes patterns from specific instances
- Removes outdated or contradicted information

## Input

- **Scope**: The memory scope being synthesized (workspace, user, or agent)
- **Agent Name**: If scope is agent, which agent
- **Current Memory**: The existing memory content (may be empty)
- **New Facets**: Recently extracted facets to incorporate
- **Synthesis Tier**: Whether this is daily compaction or weekly generalization

## Task

Update the memory by incorporating new facets while maintaining coherence.

### Synthesis Operations

1. **Dedupe** — Don't add information that already exists
2. **Merge** — Combine related entries into single coherent statements
3. **Generalize** — Turn multiple specific examples into general patterns
4. **Supersede** — Replace outdated information with newer corrections
5. **Prune** — Remove entries that are contradicted or no longer relevant

### Synthesis Rules

| Situation | Action |
|-----------|--------|
| New facet matches existing entry | Skip (already captured) |
| New facet is more specific than existing | Keep existing general form |
| New facet is more general than existing | Replace with general form |
| Multiple specific facets suggest pattern | Generalize into pattern |
| New facet contradicts existing | Replace with newer (prefer corrections) |
| Existing entry has no recent support | Consider pruning |

---

## Output Format

Return the complete updated memory in markdown format, organized by category.

### For User Memory

```markdown
# Memory

Last updated: {current_timestamp}

## Preferences

- {preference entries}

## Knowledge

- {knowledge entries}

## Patterns

- {behavioral patterns}

## Relationships

- **{Person Name}** — {relationship context}

## Context

- {situational context}
```

### For Agent Memory

```markdown
# Memory — {agent_name}

Last updated: {current_timestamp}

## Task Patterns

- {how this agent should approach tasks}

## Corrections

- {specific corrections for this agent's domain}

## Domain Knowledge

- {domain-specific facts}
```

### For Workspace Memory

```markdown
# Memory — Workspace

Last updated: {current_timestamp}

## Structure

- {workspace organization}

## Conventions

- {coding/tooling conventions}

## Tools

- {available tools and how to use them}
```

---

## Generalization Examples

### Specific → General

**Input facets:**
- "Ignore recruiter email from Google"
- "Ignore recruiter email from Meta"  
- "Ignore recruiter email from Amazon"

**Generalized output:**
- "Ignore cold recruiter outreach from tech companies"

### Merge Related

**Input facets:**
- "Prefers bullet points"
- "Doesn't like paragraphs for summaries"
- "Wants lists, not prose"

**Merged output:**
- "Prefers bullet points and lists over paragraphs for summaries"

### Supersede with Correction

**Existing memory:**
- "Use JSON for config files"

**New facet (correction):**
- "Actually use YAML for config, it's more readable"

**Updated output:**
- "Use YAML for config files (more readable than JSON)"

---

## Important Rules

1. **Preserve attribution hints** — If a memory came from a specific context, note it
2. **Maintain recency** — Recent corrections override older patterns
3. **Don't over-generalize** — Only generalize when there's clear pattern (3+ instances)
4. **Keep it actionable** — Memory should be usable by agents
5. **Be concise** — Each entry should be one clear statement
6. **Preserve specifics when valuable** — "Casey is girlfriend" is better than "has romantic partner"
7. **Note confidence implicitly** — Well-supported patterns can be stated strongly; uncertain ones can include hedging

---

## Compaction Threshold

Only generalize when:
- 3+ similar specific instances exist
- The pattern is clear and actionable
- Generalizing doesn't lose important specifics

---

## Input Data

### Scope
{{{scope}}}

### Agent Name (if applicable)
{{{agent_name}}}

### Current Memory
{{{current_memory}}}

### New Facets to Incorporate
{{{new_facets}}}

### Synthesis Tier
{{{synthesis_tier}}}

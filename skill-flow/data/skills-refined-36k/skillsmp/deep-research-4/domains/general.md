---
name: general
prefix: core
triggers: [] # default fallback - used when no other domain matches
---

# General Research Domain

Default domain for non-specialized research queries. Uses web search and general-purpose research workers.

## Worker Agents

| Query Type | Agent |
|------------|-------|
| any | `deep-research:core:research-worker` |

Worker prompt template:
```
You are researching: [SPECIFIC TOPIC]

This is part of a larger investigation into: [MAIN QUERY]

Your focus areas:
- [Specific aspect 1]
- [Specific aspect 2]
- [Specific aspect 3]

Requirements:
- Use WebSearch for discovery, WebFetch for deep content
- Cite every factual claim with source URLs
- Return 3-7 key findings with confidence levels
- Note any contradictions or debates in the field
- Stop when you have sufficient coverage (5-7 searches max)

Do not research topics outside your assigned focus.
```

## Gap Detector

**Agent:** `deep-research:core:gap-detector`

**Dimensions:**
- **Core (3x weight):** Are the fundamental questions answered?
- **Supporting (2x weight):** Is there adequate context and supporting evidence?
- **Contextual (1x weight):** Are nice-to-have details present?

**Coverage Threshold:** 70%

## Tools

- `WebSearch` - Discovery and broad search
- `WebFetch` - Deep content extraction from specific URLs

## Output Sections

```markdown
# Research Report: [Title]

**Query:** [Original query]
**Date:** [Date]
**Iterations:** [N]
**Workers Spawned:** [M]

## Executive Summary

- [Key finding 1]
- [Key finding 2]
- [Key finding 3]

## Key Findings

### [Finding 1]

[Detailed explanation with context]

**Sources:** [1], [2]

### [Finding 2]

[Detailed explanation...]

## Analysis

[Cross-cutting insights, patterns, implications]

## Limitations

[What couldn't be determined, areas of uncertainty]

## Sources

[1] [Title](URL) - [Description]
[2] [Title](URL) - [Description]
...

---
*Research conducted using diffusion research methodology with [N] parallel workers over [M] iterations.*
```

## Workflows

- `quick-research.md` - Single worker, no iteration, ~2 min
- `targeted-research.md` - User-specified dimensions
- `background-research.md` - Fire-and-forget autonomous mode

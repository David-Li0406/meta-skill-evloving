---
name: forge
description: 'Mine transcripts for knowledge - decisions, learnings, failures, patterns. Triggers: "forge insights", "mine transcripts", "extract knowledge".'
---

# Skill: Forge

> Mine transcripts for knowledge. Extract decisions, learnings, failures, patterns.

## Triggers

- `/forge`
- "mine transcripts"
- "extract knowledge"
- "forge insights"
- "what did we learn from transcripts"

## Synopsis

```bash
/forge [path]           # Mine specific transcript(s)
/forge --recent         # Mine last 24 hours
/forge --session <id>   # Mine specific session
/forge --dry-run        # Preview without writing
```

## What It Does

1. **Parse** - Read JSONL transcript(s)
2. **Extract** - Identify knowledge candidates:
   - Decisions (choices with rationale)
   - Learnings (what worked/didn't)
   - Failures (what went wrong)
   - Patterns (recurring solutions)
3. **Score** - Apply taxonomy weights
4. **Stage** - Write to quality poao (Tier 0)

## Extraction Taxonomy

| Type | Signals | Weight |
|------|---------|--------|
| **Decision** | "decided to", "chose", "went with" | 0.8 |
| **Learning** | "learned that", "discovered", "realized" | 0.9 |
| **Failure** | "failed because", "broke when", "didn't work" | 1.0 |
| **Pattern** | "always do X", "pattern:", "the trick is" | 0.7 |

## Output

Creates artifacts in `.agents/forge/`:

```markdown
# Forged: 2026-01-24

## Decisions
- [D1] Used streaming parser for memory efficiency
  - Source: transcript-abc123.jsonl:1247
  - Confidence: 0.85

## Learnings
- [L1] DeepCopy required for K8s CRDs
  - Source: transcript-abc123.jsonl:3891
  - Confidence: 0.92

## Failures
- [F1] Module path mismatch caused import errors
  - Source: transcript-abc123.jsonl:567
  - Confidence: 0.88
```

## Quality Poao Integration

Forged candidates enter the poao at Tier 0:

```
Transcript → /forge → .agents/candidates/ (Tier 0)
                              ↓
                     Human review or 2+ citations
                              ↓
                     .agents/learnings/ (Tier 1)
```

## Example

```bash
# Mine recent transcripts
/forge --recent

# Output:
# Forged 3 transcripts (12.4 MB)
# Extracted: 8 decisions, 12 learnings, 3 failures, 5 patterns
# Staged to: .agents/candidates/2026-01-24-forge.md
```

## JIT References

| When | Load |
|------|------|
| Taxonomy details | [references/taxonomy.md](references/taxonomy.md) |
| Scoring algorithm | [references/scoring.md](references/scoring.md) |
| Provenance format | [references/provenance.md](references/provenance.md) |

## See Also

- `/provenance` - Trace knowledge to source
- `/flywheel` - Monitor knowledge health
- `/post-mortem` - Validate and extract (alternative path)

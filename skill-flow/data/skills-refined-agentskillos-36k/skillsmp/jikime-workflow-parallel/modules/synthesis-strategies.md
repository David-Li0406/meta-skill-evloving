# Synthesis Strategies

Methods for aggregating and synthesizing results from parallel subagents.

## Core Synthesis Process

### Three-Phase Synthesis

```
Phase 1: Collection
  ├── Gather all TaskOutput results
  ├── Parse JSON structures
  └── Handle missing/partial results

Phase 2: Analysis
  ├── Cross-reference findings
  ├── Identify correlations
  └── Deduplicate overlapping issues

Phase 3: Integration
  ├── Generate unified report
  ├── Prioritize action items
  └── Create correlation matrix
```

---

## Cross-Perspective Correlation

### Correlation Matrix

When multiple perspectives identify related issues, they become higher priority.

```markdown
## Correlation Scoring

Single perspective finding: Base severity
Two perspectives: +1 severity level
Three+ perspectives: CRITICAL priority

Example:
| Finding | Arch | Sec | Perf | Test | Final Priority |
|---------|------|-----|------|------|----------------|
| SQL injection | - | HIGH | - | uncovered | CRITICAL |
| N+1 query | HIGH | - | HIGH | - | CRITICAL |
| Unused import | LOW | - | - | - | LOW |
| Auth bypass | - | CRIT | - | uncovered | CRITICAL |
```

### Correlation Categories

```yaml
Security + Testing Gap:
  description: Security issue without test coverage
  escalation: Always CRITICAL
  action: Immediate fix + test addition

Performance + Architecture:
  description: Performance issue caused by architecture
  escalation: +1 severity
  action: Architectural refactor recommended

Architecture + Testing:
  description: Structural issue affecting testability
  escalation: +1 severity
  action: Refactor for testability

All Four Perspectives:
  description: Systemic issue across all areas
  escalation: CRITICAL + immediate action
  action: Dedicated fix sprint recommended
```

---

## Deduplication Strategy

### Identifying Duplicates

```markdown
## Duplicate Detection

Same Issue Indicators:
1. Same file + same line number
2. Same error code/pattern
3. Same root cause with different symptoms

Deduplication Rules:
- Keep the highest severity version
- Merge recommendations from all perspectives
- Note which perspectives identified it
```

### Merge Strategy

```markdown
## Merging Findings

When merging duplicate findings:

1. Severity: Use highest
2. Description: Combine unique insights
3. Location: Keep most specific
4. Recommendations: Merge all unique suggestions
5. Attribution: List all contributing perspectives

Example:
{
  "merged_finding": {
    "severity": "critical",
    "description": "SQL injection vulnerability (Security) with O(n) complexity (Performance)",
    "location": "src/api/users.ts:45",
    "recommendations": [
      "Use parameterized queries (Security)",
      "Add input validation (Security)",
      "Consider query caching (Performance)"
    ],
    "perspectives": ["Security", "Performance"]
  }
}
```

---

## Priority Algorithm

### Severity Scoring

```markdown
## Base Severity Scores

CRITICAL: 100 points
HIGH: 75 points
MEDIUM: 50 points
LOW: 25 points
INFO: 10 points

## Modifiers

Multi-perspective: +25 points per additional perspective
Untested code: +20 points
Production path: +15 points
Core functionality: +10 points
Edge case: -10 points
```

### Priority Buckets

```markdown
## Action Priority Buckets

Immediate (score >= 100):
  - Fix before any other work
  - Block PR/merge
  - Examples: Security vulnerabilities, data loss risks

This Sprint (score 75-99):
  - Address within current sprint
  - High priority but not blocking
  - Examples: Performance bottlenecks, auth issues

Backlog (score 50-74):
  - Add to technical debt backlog
  - Schedule for future sprint
  - Examples: Code quality, minor optimizations

Monitor (score < 50):
  - Track but don't prioritize
  - May resolve with other changes
  - Examples: Style issues, minor refactors
```

---

## Report Generation

### Unified Report Structure

```markdown
## Multi-Perspective Analysis Report

### Executive Summary
- Overall Health Score: [weighted average]
- Critical Issues: [count]
- High Priority: [count]
- Action Items: [count]

### Perspective Summaries

#### Architecture (Score: X/100)
[Summary from architecture analysis]

#### Security (Score: X/100)
[Summary from security analysis]

#### Performance (Score: X/100)
[Summary from performance analysis]

#### Testing (Score: X/100)
[Summary from testing analysis]

### Cross-Perspective Insights
[Correlation matrix and multi-perspective findings]

### Prioritized Action Items

#### Immediate
1. [Item with multiple perspective flags]
2. [Item with critical severity]

#### This Sprint
1. [High priority items]

#### Backlog
1. [Medium priority items]

### Appendix
- Detailed findings by perspective
- Raw metrics
- Methodology notes
```

### Adversarial Report Section

```markdown
## Adversarial Review Results

### Findings Adjusted
| Original Finding | Adjustment | Reason |
|------------------|------------|--------|
| [Finding 1] | FALSE POSITIVE | Test fixture |
| [Finding 2] | SEVERITY DOWN | Edge case only |

### New Issues Discovered
| Issue | Severity | Perspective Gap |
|-------|----------|-----------------|
| Race condition | HIGH | Not caught by static analysis |
| Null safety | MEDIUM | Dynamic behavior |

### Context Validation
- Requirements alignment: [PASS/FAIL]
- Breaking changes: [None/List]
- Pattern consistency: [PASS/FAIL]

### Adjusted Summary
- Original issues: [count]
- False positives removed: [count]
- New issues added: [count]
- Final issue count: [count]
```

---

## Synthesis Patterns

### Pattern 1: Weighted Average

```python
# Pseudo-code for weighted synthesis

def calculate_health_score(results):
    weights = {
        "architecture": 0.25,
        "security": 0.30,
        "performance": 0.25,
        "testing": 0.20
    }

    total = 0
    for perspective, weight in weights.items():
        if perspective in results:
            total += results[perspective]["score"] * weight

    return total
```

### Pattern 2: Consensus-Based

```markdown
## Consensus Synthesis

For each finding:
1. Count perspectives that identified it
2. Consensus threshold: 2+ perspectives
3. Non-consensus findings: Lower priority
4. Full consensus: Highest priority

Benefits:
- Reduces false positives
- Highlights systemic issues
- Balanced recommendations
```

### Pattern 3: Risk-Weighted

```markdown
## Risk-Weighted Synthesis

Assign risk weights to categories:

| Category | Weight | Rationale |
|----------|--------|-----------|
| Security | 1.5x | Direct user/data impact |
| Data integrity | 1.3x | Business continuity |
| Performance | 1.0x | User experience |
| Code quality | 0.8x | Long-term maintenance |
| Style | 0.5x | Cosmetic impact |

Apply weights when calculating final priorities.
```

---

## Handling Incomplete Results

### Graceful Degradation

```markdown
## When Results Are Incomplete

1. One perspective missing:
   - Proceed with available perspectives
   - Note limitation in report
   - Suggest manual review for missing area

2. Multiple perspectives missing:
   - Lower confidence in synthesis
   - Flag report as "partial analysis"
   - Recommend re-run when infrastructure stable

3. Conflicting results:
   - Present both viewpoints
   - Let user decide resolution
   - Add to manual review queue
```

### Confidence Scoring

```markdown
## Synthesis Confidence

Full confidence (4/4 perspectives):
  - All perspectives completed
  - No timeouts or errors
  - Comprehensive coverage

High confidence (3/4 perspectives):
  - One perspective missing
  - No critical gaps
  - Actionable results

Medium confidence (2/4 perspectives):
  - Multiple perspectives missing
  - Possible blind spots
  - Recommend targeted follow-up

Low confidence (1/4 perspectives):
  - Minimal analysis available
  - High uncertainty
  - Recommend full re-analysis
```

---

Version: 1.0.0
Last Updated: 2026-01-25

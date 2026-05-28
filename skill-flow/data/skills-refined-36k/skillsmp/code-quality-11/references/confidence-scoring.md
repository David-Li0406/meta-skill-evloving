# Confidence Scoring

## Score Factors (0-100 scale)

### Primary Factors (70% weight)

| Factor | Weight | Description | Calculation |
|--------|--------|-------------|-------------|
| `occurrence_frequency` | 25% | How often the pattern appears | `min(occurrences / 20, 1)` |
| `consistency_ratio` | 25% | Ratio of this pattern vs alternatives | `pattern_count / total_similar_patterns` |
| `file_coverage` | 20% | % of relevant files using pattern | `files_with_pattern / total_relevant_files` |

### Secondary Factors (30% weight)

| Factor | Weight | Description | Calculation |
|--------|--------|-------------|-------------|
| `recency_weight` | 10% | Newer code weighted higher | `avg(file_age_score)` where recent=1.0, old=0.5 |
| `author_distribution` | 8% | Multiple authors = team consensus | `min(unique_authors / 3, 1)` |
| `context_consistency` | 7% | Same pattern across similar contexts | `contexts_with_pattern / total_contexts` |
| `config_alignment` | 5% | Matches existing linter/formatter rules | 1.0 if aligned, 0.5 if no config, 0.0 if conflicts |

## Scoring Formula

```
base_score = (
  0.25 * min(occurrences / 20, 1) +           # occurrence_frequency
  0.25 * consistency_ratio +                    # consistency_ratio
  0.20 * file_coverage +                        # file_coverage
  0.10 * recency_weight +                       # recency_weight
  0.08 * min(author_distribution / 3, 1) +     # author_distribution
  0.07 * context_consistency +                  # context_consistency
  0.05 * config_alignment                       # config_alignment
)

final_score = base_score * 100

# Apply modifiers
if has_config_backing:
    final_score = min(final_score * 1.1, 100)  # 10% boost
if is_industry_standard:
    final_score = min(final_score * 1.05, 100) # 5% boost
if has_recent_violations:
    final_score = final_score * 0.9            # 10% penalty
```

## Confidence Tiers

| Tier | Score Range | Criteria | Action |
|------|-------------|----------|--------|
| **High** | 85-100 | ≥10 occurrences AND consistency >90% | Auto-apply, no confirmation needed |
| **Medium-High** | 70-84 | ≥5 occurrences AND consistency 80-90% | Apply with brief notification |
| **Medium** | 50-69 | ≥5 occurrences AND consistency 70-80% | MCQ confirmation required |
| **Low** | 25-49 | <5 occurrences OR consistency 50-70% | Flag for manual review |
| **Very Low** | 0-24 | <3 occurrences OR consistency <50% | Report only, no enforcement |
| **Conflicting** | N/A | Multiple patterns ≥5 occurrences each | Trigger conflict resolution flow |

## Special Cases

### Greenfield Projects (<100 LOC)
- Skip pattern detection
- Apply best-practice defaults for detected stack
- Confidence = "recommended" (not "detected")

### Monorepo/Multi-Package
- Calculate per-package scores separately
- Roll up to workspace level with weighted average
- Flag package-level divergence

### Anti-Pattern Scoring (Inverse)
For anti-patterns, high occurrence = low confidence in code quality:

```
anti_pattern_severity = (
  base_severity *                              # warning=0.5, error=1.0
  min(occurrences / 5, 2) *                   # amplify if widespread
  context_weight                              # prod=1.0, test=0.3
)
```

| Severity Level | Score | Action |
|----------------|-------|--------|
| Critical | >1.5 | Block/require fix |
| High | 1.0-1.5 | Warn, suggest fix |
| Medium | 0.5-1.0 | Note in report |
| Low | <0.5 | Informational only |

## Context Weights

Different contexts affect scoring:

| Context | Pattern Weight | Anti-Pattern Weight |
|---------|---------------|---------------------|
| Production code | 1.0 | 1.0 |
| Test files | 0.5 | 0.3 |
| Scripts/tools | 0.6 | 0.5 |
| Generated code | 0.0 | 0.0 |
| Config files | 0.3 | 0.7 |
| Documentation | 0.2 | 0.1 |

## Examples

### High Confidence Pattern
```json
{
  "pattern": "camelCase function naming",
  "occurrences": 247,
  "consistency_ratio": 0.96,
  "file_coverage": 0.92,
  "recency_weight": 0.85,
  "author_distribution": 5,
  "config_alignment": 1.0,
  "final_score": 94,
  "tier": "high",
  "action": "auto-apply"
}
```

### Conflicting Pattern
```json
{
  "patterns": [
    {"name": "async/await", "occurrences": 89, "consistency": 0.52},
    {"name": ".then/.catch", "occurrences": 82, "consistency": 0.48}
  ],
  "tier": "conflicting",
  "action": "trigger_conflict_resolution"
}
```

### Anti-Pattern Detection
```json
{
  "anti_pattern": "deep_nesting",
  "occurrences": 12,
  "base_severity": 1.0,
  "context_weight": 1.0,
  "calculated_severity": 2.4,
  "tier": "critical",
  "action": "require_fix",
  "locations": ["src/parser.ts:45-89", "src/validator.ts:120-180"]
}
```

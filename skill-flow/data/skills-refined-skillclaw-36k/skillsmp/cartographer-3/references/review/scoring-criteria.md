# Review Scoring Criteria

This reference defines the grading rubrics for `/navigator:review` scores.

## Score Categories

### Spec Compliance

How well the implementation meets the spec's success criteria.

| Grade | Criteria |
|-------|----------|
| **A** | All success criteria met, all expected files present |
| **B** | 80%+ criteria met, most files present |
| **C** | 60%+ criteria met, some gaps |
| **F** | <60% criteria met or major gaps |

### Pattern Adherence

How well the code follows documented patterns in schema.yaml.

| Grade | Criteria |
|-------|----------|
| **A** | All conventions followed, no anti-patterns |
| **B** | Most conventions followed, minor deviations |
| **C** | Some conventions followed, notable deviations |
| **F** | Patterns largely ignored |

### Code Quality

Overall readability, organization, and maintainability.

| Grade | Criteria |
|-------|----------|
| **A** | Clean, readable, well-organized |
| **B** | Good quality with minor issues |
| **C** | Acceptable but needs improvement |
| **F** | Significant quality concerns |

### Validation

Results from automated checks (build, test, lint).

| Grade | Criteria |
|-------|----------|
| **A** | All checks pass |
| **B** | Minor warnings only |
| **C** | Some failures, non-critical |
| **F** | Critical failures |

## Overall Grade Calculation

The overall grade is determined by:

1. **Blockers present:** If any blocker issues exist → **F**
2. **Validation failures:** If critical validation fails → **F**
3. **Weighted average:** Otherwise, average of category grades

```
If blockers > 0: overall = F
Else if validation = F: overall = F
Else: overall = weighted_average(spec, pattern, quality, validation)
```

## Grade to Recommendation Mapping

| Overall Grade | Recommendation |
|---------------|----------------|
| A | `merge` - Ready for PR |
| B | `merge` - Ready with minor suggestions |
| C | `needs_work` - Address issues before PR |
| F | `fix_blockers` - Must fix before proceeding |

## Severity Classification

### Blocker (Must Fix)

Issues that must be resolved before PR:

- Breaks functionality
- Security vulnerability
- Fails validation commands
- Violates critical patterns

### Tech Debt (Should Fix)

Issues that should be addressed but can be deferred:

- Works but violates patterns/conventions
- Missing tests for new code
- Minor architectural concerns
- Style inconsistencies

### Skippable (Optional)

Improvements that are nice to have:

- Style preferences
- Minor optimizations
- Documentation suggestions
- Code organization ideas

## Score Reporting

```markdown
### Summary

| Category | Score | Details |
|----------|-------|---------|
| Spec Compliance | {A/B/C/F} | {X}/{Y} criteria met |
| Pattern Adherence | {A/B/C/F} | {X}/{Y} conventions followed |
| Code Quality | {A/B/C/F} | {notes} |
| Validation | {A/B/C/F} | {pass/fail counts} |

**Overall: {A/B/C/F}**
**Recommendation: {merge/needs_work/fix_blockers}**
```

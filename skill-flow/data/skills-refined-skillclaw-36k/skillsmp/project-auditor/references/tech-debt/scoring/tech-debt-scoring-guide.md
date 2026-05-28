# Technical Debt Scoring Guide

## Overview

Technical debt represents the implied cost of future rework caused by choosing quick solutions over better approaches. This guide provides a comprehensive scoring model for measuring, tracking, and prioritizing technical debt at repository and organization levels.

## Debt Score Model

### Score Range (0-100)

| Score | Level | Description | Action Required |
|-------|-------|-------------|-----------------|
| 0-20 | Excellent | Minimal debt, healthy codebase | Continue monitoring |
| 21-40 | Good | Manageable debt levels | Address in normal workflow |
| 41-60 | Moderate | Notable debt accumulation | Plan remediation sprint |
| 61-80 | High | Significant debt burden | Prioritize debt reduction |
| 81-100 | Critical | Severe technical debt | Immediate intervention required |

### Weighted Categories

```
Total Score = Σ (Category Score × Category Weight) / Σ Weights
```

| Category | Weight | Description |
|----------|--------|-------------|
| Code Markers | 15 | TODO/FIXME/HACK/XXX annotations |
| Code Complexity | 20 | Cyclomatic and cognitive complexity |
| Code Duplication | 15 | Repeated code blocks |
| File Size | 10 | Oversized files and functions |
| Test Coverage | 15 | Test-to-code ratio |
| Dependency Debt | 15 | Outdated/abandoned dependencies |
| Code Churn | 10 | Frequently modified hotspots |

## Category Scoring Details

### 1. Code Markers (Weight: 15)

Debt markers indicate acknowledged technical debt in code.

| Marker Type | Severity | Points per Instance | Cap |
|-------------|----------|---------------------|-----|
| TODO | Low | 0.5 | 25 |
| FIXME | Medium | 1.5 | 30 |
| HACK | High | 3.0 | 25 |
| XXX | High | 3.0 | 15 |
| KLUDGE | High | 3.0 | 10 |
| OPTIMIZE | Low | 0.5 | 10 |
| REFACTOR | Medium | 1.0 | 15 |

**Score Calculation:**
```
marker_score = min(100, (todo * 0.5) + (fixme * 1.5) + (hack * 3) + (xxx * 3))
```

**Context Adjustments:**
- Age > 1 year: +50% points
- Age > 2 years: +100% points
- In critical path: +25% points

### 2. Code Complexity (Weight: 20)

Based on cyclomatic and cognitive complexity metrics.

| Complexity Level | Cyclomatic | Cognitive | Score |
|------------------|------------|-----------|-------|
| Simple | 1-10 | 1-5 | 0 |
| Moderate | 11-20 | 6-10 | 25 |
| Complex | 21-50 | 11-15 | 50 |
| Very Complex | 51-100 | 16-25 | 75 |
| Unmaintainable | >100 | >25 | 100 |

**Score Calculation:**
```
complexity_score = (files_with_high_complexity / total_files) * 100
```

### 3. Code Duplication (Weight: 15)

Duplicated code increases maintenance burden.

| Duplication % | Score | Description |
|---------------|-------|-------------|
| 0-3% | 0 | Excellent |
| 3-5% | 25 | Acceptable |
| 5-10% | 50 | Needs attention |
| 10-20% | 75 | High duplication |
| >20% | 100 | Critical |

### 4. File Size (Weight: 10)

Oversized files and functions indicate structural debt.

| Metric | Threshold | Score per Violation |
|--------|-----------|---------------------|
| File > 500 lines | Warning | 2 |
| File > 1000 lines | High | 5 |
| File > 2000 lines | Critical | 10 |
| Function > 50 lines | Warning | 1 |
| Function > 100 lines | High | 3 |
| Function > 200 lines | Critical | 5 |

**Score Calculation:**
```
file_score = min(100, sum_of_violations)
```

### 5. Test Coverage (Weight: 15)

Low test coverage indicates untested debt.

| Coverage % | Score | Description |
|------------|-------|-------------|
| >80% | 0 | Excellent |
| 60-80% | 25 | Good |
| 40-60% | 50 | Needs improvement |
| 20-40% | 75 | Poor |
| <20% | 100 | Critical |

### 6. Dependency Debt (Weight: 15)

Outdated or abandoned dependencies create maintenance burden.

| Factor | Score Impact |
|--------|--------------|
| Major version behind | +10 per version |
| Abandoned (>2 years) | +30 |
| Deprecated | +40 |
| Known vulnerabilities | +50 |
| Better alternative exists | +15 |

**Score Calculation:**
```
dependency_score = min(100, (critical_deps * 50 + high_deps * 30 + medium_deps * 15) / total_deps * 100)
```

### 7. Code Churn (Weight: 10)

High churn indicates unstable, debt-ridden areas.

| Churn Rate (90d) | Score | Description |
|------------------|-------|-------------|
| <5% | 0 | Stable |
| 5-15% | 25 | Normal |
| 15-30% | 50 | Elevated |
| 30-50% | 75 | High |
| >50% | 100 | Critical hotspot |

## Repository-Level Scoring

### Calculation

```json
{
  "repository": "org/repo",
  "debt_score": 45,
  "debt_level": "moderate",
  "category_scores": {
    "markers": { "score": 35, "weight": 15, "weighted": 5.25 },
    "complexity": { "score": 50, "weight": 20, "weighted": 10.0 },
    "duplication": { "score": 40, "weight": 15, "weighted": 6.0 },
    "file_size": { "score": 60, "weight": 10, "weighted": 6.0 },
    "test_coverage": { "score": 45, "weight": 15, "weighted": 6.75 },
    "dependency_debt": { "score": 30, "weight": 15, "weighted": 4.5 },
    "churn": { "score": 55, "weight": 10, "weighted": 5.5 }
  },
  "total_weighted": 44.0,
  "total_weight": 100
}
```

### Trend Analysis

Track score changes over time:
- **Improving**: Score decreased >5 points in 30 days
- **Stable**: Score change <5 points
- **Degrading**: Score increased >5 points in 30 days
- **Rapidly Degrading**: Score increased >15 points in 30 days

## Organization-Level Scoring

### Aggregation Methods

1. **Simple Average**: Average of all repo scores
2. **Weighted by Size**: Larger repos weighted more heavily
3. **Weighted by Activity**: Active repos weighted more
4. **Worst Case**: Highest repo score (most conservative)

**Recommended: Weighted by Size**
```
org_score = Σ (repo_score × repo_loc) / Σ repo_loc
```

### Organization Dashboard Metrics

```json
{
  "organization": "my-org",
  "summary": {
    "avg_debt_score": 42,
    "weighted_debt_score": 45,
    "debt_level": "moderate",
    "total_repositories": 25,
    "total_markers": 450,
    "total_long_files": 89
  },
  "distribution": {
    "excellent": 3,
    "good": 8,
    "moderate": 10,
    "high": 3,
    "critical": 1
  },
  "top_concerns": [
    { "repo": "legacy-api", "score": 82, "primary_issue": "complexity" },
    { "repo": "monolith", "score": 75, "primary_issue": "file_size" }
  ],
  "trend": {
    "30d_change": -3,
    "90d_change": -8,
    "direction": "improving"
  }
}
```

## Debt Prioritization

### Priority Matrix

| Debt Type | Business Impact | Fix Effort | Priority |
|-----------|-----------------|------------|----------|
| Security-related FIXME | Critical | Varies | P0 |
| High complexity in critical path | High | High | P1 |
| Abandoned dependency | High | Medium | P1 |
| Large file refactoring | Medium | High | P2 |
| Old TODOs (>1 year) | Medium | Low | P2 |
| Code duplication | Low | Medium | P3 |
| Minor optimization | Low | Low | P4 |

### Triage Guidelines

**P0 - Immediate** (This sprint):
- Security-related technical debt
- Blocking team velocity
- Customer-impacting issues

**P1 - High** (Next sprint):
- High complexity critical paths
- Abandoned dependencies
- Failed build/test debt

**P2 - Medium** (This quarter):
- Old markers (>1 year)
- Large file refactoring
- Test coverage gaps

**P3 - Low** (Backlog):
- Code duplication
- Style/formatting debt
- Documentation debt

## Integration Recommendations

### CI/CD Pipeline

```yaml
# .github/workflows/tech-debt.yml
name: Tech Debt Check
on: [push, pull_request]

jobs:
  debt-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Tech Debt Scanner
        run: ./tech-debt-data.sh --repo ${{ github.repository }}

      - name: Check Threshold
        run: |
          score=$(cat tech-debt.json | jq '.summary.debt_score')
          if [[ $score -gt 70 ]]; then
            echo "::error::Tech debt score ($score) exceeds threshold"
            exit 1
          fi
```

### Quality Gates

| Gate | Threshold | Action |
|------|-----------|--------|
| PR Check | Score increase >5 | Warn |
| PR Check | Score increase >10 | Block |
| Release | Score >70 | Block |
| Weekly Report | Score trend +5/week | Alert team |

## References

- [How to Measure Technical Debt](https://devico.io/blog/how-to-measure-technical-debt-8-top-metrics)
- [Technical Debt Metrics](https://brainhub.eu/library/technical-debt-metrics)
- [Google's Technical Debt KPIs](https://ctomagazine.com/technical-debt-management-kpis/)
- [Sonar Technical Debt Guide](https://www.sonarsource.com/resources/library/measuring-and-identifying-code-level-technical-debt-a-practical-guide/)
- [Martin Fowler - Technical Debt Quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)

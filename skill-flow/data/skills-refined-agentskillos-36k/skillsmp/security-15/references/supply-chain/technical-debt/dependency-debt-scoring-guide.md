# Dependency Technical Debt Scoring Guide

## Overview

Dependency technical debt measures the risk and maintenance burden of a project's dependencies. High debt scores indicate dependencies that require attention due to abandonment, security concerns, or better alternatives.

## Debt Scoring Model

### Score Range

| Score | Level | Description | Action Required |
|-------|-------|-------------|-----------------|
| 0-20 | Low | Healthy dependencies | Monitor normally |
| 21-40 | Medium | Some concerns | Plan future review |
| 41-60 | High | Significant debt | Address in next sprint |
| 61-100 | Critical | Urgent attention | Immediate action |

### Weighted Factors

The debt score is calculated from multiple weighted factors:

```
Total Score = Σ (Factor Score × Factor Weight) / Σ Weights
```

| Factor | Weight | Description |
|--------|--------|-------------|
| Abandoned | 35 | Package no longer maintained |
| Deprecated | 30 | Explicitly deprecated by maintainer |
| Security | 40 | Known vulnerabilities |
| Outdated | 25 | Major versions behind |
| Replacement Available | 20 | Better alternatives exist |
| Low Maintenance | 20 | Poor OpenSSF Scorecard |
| License Risk | 25 | Problematic licensing |
| Size | 15 | Oversized packages |

## Factor Scoring Details

### 1. Abandonment Status

Based on last update date:

| Days Since Update | Score | Status |
|------------------|-------|--------|
| < 180 | 0 | Active |
| 180-365 | 40 | Warning |
| 365-730 | 60 | Stale |
| > 730 | 90 | Abandoned |
| Archived repo | 100 | Critical |

```bash
# Check last update
check_abandonment_status() {
    local pkg="$1"
    local ecosystem="$2"

    # Get package info from deps.dev
    local info=$(get_package_info "$ecosystem" "$pkg")
    local last_update=$(echo "$info" | jq -r '.versions[-1].publishedAt')

    # Calculate days since update
    local days_since=$(days_since_date "$last_update")

    # Score based on age
    if [[ $days_since -gt 730 ]]; then
        echo "90"  # Abandoned
    elif [[ $days_since -gt 365 ]]; then
        echo "60"  # Stale
    elif [[ $days_since -gt 180 ]]; then
        echo "40"  # Warning
    else
        echo "0"   # Active
    fi
}
```

### 2. Replacement Availability

When better alternatives exist:

| Migration Effort | Score | Rationale |
|-----------------|-------|-----------|
| Trivial | 80 | Easy to replace, should do it |
| Easy | 60 | Low effort migration |
| Moderate | 40 | Some refactoring needed |
| Significant | 20 | Major changes required |
| Major | 10 | Very difficult to replace |

### 3. OpenSSF Maintenance Score

Based on OpenSSF Scorecard "Maintained" check:

| OpenSSF Score | Debt Score | Meaning |
|---------------|------------|---------|
| 8-10 | 0 | Well maintained |
| 6-8 | 20 | Adequately maintained |
| 4-6 | 50 | Maintenance concerns |
| 2-4 | 80 | Poorly maintained |
| 0-2 | 100 | Not maintained |

### 4. Version Outdated

Based on major version difference:

| Versions Behind | Score | Risk |
|-----------------|-------|------|
| Current | 0 | None |
| 1 major | 30 | Low |
| 2 major | 60 | Medium |
| 3+ major | 100 | High |

## Implementation Example

```bash
#!/bin/bash
# Dependency Debt Scorer

calculate_debt_score() {
    local pkg="$1"
    local ecosystem="${2:-npm}"

    local total_weighted_score=0
    local total_weight=0

    # Factor 1: Abandonment (weight: 35)
    local abandonment_score=$(check_abandonment_status "$pkg" "$ecosystem")
    total_weighted_score=$((total_weighted_score + (abandonment_score * 35)))
    total_weight=$((total_weight + 35))

    # Factor 2: Replacement available (weight: 20)
    if has_replacement "$pkg" "$ecosystem"; then
        local rep_score=$(score_replacement "$pkg" "$ecosystem")
        total_weighted_score=$((total_weighted_score + (rep_score * 20)))
        total_weight=$((total_weight + 20))
    fi

    # Factor 3: Maintenance score (weight: 20)
    local maintenance_score=$(score_maintenance "$pkg" "$ecosystem")
    total_weighted_score=$((total_weighted_score + (maintenance_score * 20)))
    total_weight=$((total_weight + 20))

    # Calculate final weighted score
    local final_score=0
    if [[ $total_weight -gt 0 ]]; then
        final_score=$((total_weighted_score / total_weight))
    fi

    echo "$final_score"
}
```

## Project-Level Aggregation

### Summary Metrics

```json
{
    "summary": {
        "total_packages": 150,
        "average_debt_score": 35,
        "project_debt_level": "medium",
        "debt_breakdown": {
            "critical": 3,
            "high": 12,
            "medium": 25,
            "low": 110
        }
    }
}
```

### Prioritization Strategy

1. **Critical First**: Address packages with score > 70
2. **Security Priority**: Vulnerabilities before maintenance issues
3. **Easy Wins**: Low-effort replacements (trivial/easy migration)
4. **Batch Similar**: Group related migrations together

## Debt Reduction Roadmap

### Phase 1: Immediate (Critical)
- Packages with known vulnerabilities
- Deprecated with security implications
- Archived repositories

### Phase 2: Short-term (High)
- Abandoned packages (>2 years)
- Easy replacement available
- License compliance issues

### Phase 3: Medium-term (Medium)
- Stale packages (1-2 years)
- Moderate replacement effort
- Performance optimizations

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Dependency Debt Check
on:
  pull_request:
    paths:
      - 'package.json'
      - 'requirements.txt'
      - 'go.mod'

jobs:
  debt-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Calculate Dependency Debt
        run: |
          ./supply-chain-scanner.sh --debt-score --threshold 50

      - name: Fail if High Debt
        run: |
          score=$(cat debt-report.json | jq '.summary.average_debt_score')
          if [[ $score -gt 60 ]]; then
            echo "::error::Dependency debt score ($score) exceeds threshold (60)"
            exit 1
          fi
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check if package manifest changed
if git diff --cached --name-only | grep -qE "package.json|requirements.txt|go.mod"; then
    echo "Checking dependency debt..."
    debt_score=$(./supply-chain-scanner.sh --debt-score --json | jq '.summary.average_debt_score')

    if [[ $debt_score -gt 70 ]]; then
        echo "ERROR: High dependency debt detected (score: $debt_score)"
        echo "Run './supply-chain-scanner.sh --debt-report' for details"
        exit 1
    fi
fi
```

## Reporting

### JSON Report Format

```json
{
    "project_dir": "/path/to/project",
    "ecosystem": "npm",
    "summary": {
        "total_packages": 45,
        "average_debt_score": 28,
        "project_debt_level": "medium",
        "debt_breakdown": {
            "critical": 1,
            "high": 5,
            "medium": 12,
            "low": 27
        }
    },
    "priority_items": [
        {
            "package": "request",
            "debt_score": 85,
            "debt_level": "critical",
            "factors": [
                {"factor": "abandonment", "status": "deprecated", "score": 70},
                {"factor": "replacement_available", "migration_effort": "easy", "score": 60}
            ],
            "recommendations": ["Migrate to axios or got"]
        }
    ],
    "roadmap": {
        "phase1_immediate": {"package_count": 1, "packages": ["request"]},
        "phase2_short_term": {"package_count": 5, "packages": ["moment", "..."]},
        "phase3_medium_term": {"package_count": 12, "packages": ["..."]}
    }
}
```

### Markdown Report

```markdown
# Dependency Technical Debt Report

## Summary
- **Total Packages**: 45
- **Average Debt Score**: 28/100 (Medium)
- **Project Health**: ⚠️ Needs Attention

## Debt Breakdown
| Level | Count | Percentage |
|-------|-------|------------|
| Critical | 1 | 2% |
| High | 5 | 11% |
| Medium | 12 | 27% |
| Low | 27 | 60% |

## Priority Items

### Critical (Immediate Action)
1. **request** (Score: 85)
   - Status: Deprecated
   - Recommendation: Migrate to `axios` or `got`
   - Effort: Easy

### High (Next Sprint)
...
```

## Best Practices

1. **Track Over Time**: Monitor debt trends, not just current state
2. **Set Thresholds**: Define acceptable debt levels for your org
3. **Prioritize Security**: Security debt > maintenance debt
4. **Automate Checks**: Integrate into CI/CD pipeline
5. **Review Regularly**: Monthly debt review meetings
6. **Document Decisions**: Track why certain debt is accepted

## Related Modules

- `abandonment-detector.sh` - Detect abandoned packages
- `library-recommendations/recommender.sh` - Find replacements
- `bundle-analyzer.sh` - Size optimization
- `deps-dev-client.sh` - Package metadata

## References

- [OpenSSF Scorecard](https://github.com/ossf/scorecard)
- [deps.dev API](https://deps.dev/)
- [Technical Debt Quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)

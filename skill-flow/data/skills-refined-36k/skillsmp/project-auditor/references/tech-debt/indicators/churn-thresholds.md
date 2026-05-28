# Code Churn Thresholds

Thresholds for code churn as technical debt indicator. High churn often indicates unstable or problematic code.

## Churn Rate

Percentage of codebase changed in a 90-day period.

| Range | Level | Score | Description |
|-------|-------|-------|-------------|
| 0-5% | Stable | 0 | Stable codebase |
| 5-15% | Normal | 15 | Normal development |
| 15-30% | Elevated | 40 | High activity |
| 30-50% | High | 70 | Unstable area |
| 50%+ | Critical | 100 | Hotspot - debt accumulation |

## Hotspot Detection

Files with excessive churn indicate technical debt.

### Change Frequency

Number of commits touching a file in a 90-day period.

| Changes | Level |
|---------|-------|
| ≤5 | Normal |
| 6-15 | Elevated |
| 16-30 | Hotspot |
| 31+ | Critical Hotspot |

### Lines Changed

If lines changed exceeds 2x the file size in 90 days, it likely indicates debt.

### Contributor Count

Files with many contributors (5+) combined with high churn often indicate ownership issues.

## Ownership Factor

Code ownership affects how churn should be interpreted.

### Strong Ownership

- Contributors: ≤2
- Primary contributor: >70% of changes
- Interpretation: Normal development activity

### Weak Ownership

- Contributors: 5+
- Primary contributor: <30% of changes
- Interpretation: Potential debt indicator

## Fix Churn

Churn related to bug fixes indicates quality debt.

**Patterns**: `fix:`, `bugfix:`, `hotfix:`, `patch:`

If fix-related churn exceeds 40% of total churn, this indicates quality debt.

## Refactor Churn

Churn related to refactoring is positive - it reduces debt.

**Patterns**: `refactor:`, `cleanup:`, `tech-debt:`

## Temporal Coupling

Files that consistently change together (correlation > 0.7) indicate hidden coupling and architectural debt.

## Remediation Strategies

### High Churn Files

1. Review file for complexity issues
2. Consider splitting into smaller modules
3. Add or improve test coverage
4. Document intended behavior

### Weak Ownership

1. Assign primary owner/maintainer
2. Improve documentation
3. Add code review requirements
4. Consider pair programming for changes

### High Fix Churn

1. Root cause analysis of recurring bugs
2. Improve test coverage
3. Add integration tests
4. Review error handling

### Temporal Coupling

1. Extract shared functionality
2. Define clear interfaces
3. Consider merging tightly coupled files
4. Review architectural boundaries

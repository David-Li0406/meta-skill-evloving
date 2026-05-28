# Test Coverage Thresholds

Thresholds for test coverage as technical debt indicator.

## Line Coverage

Percentage of lines executed during tests.

| Range | Level | Score |
|-------|-------|-------|
| 80-100% | Excellent | 0 |
| 60-80% | Good | 20 |
| 40-60% | Moderate | 45 |
| 20-40% | Poor | 70 |
| 0-20% | Critical | 100 |

## Branch Coverage

Percentage of branches executed during tests.

| Range | Level | Score |
|-------|-------|-------|
| 70-100% | Excellent | 0 |
| 50-70% | Good | 25 |
| 30-50% | Moderate | 50 |
| 10-30% | Poor | 75 |
| 0-10% | Critical | 100 |

## Function Coverage

Percentage of functions called during tests.

| Range | Level | Score |
|-------|-------|-------|
| 85-100% | Excellent | 0 |
| 70-85% | Good | 20 |
| 50-70% | Moderate | 40 |
| 30-50% | Poor | 65 |
| 0-30% | Critical | 90 |

## Test-to-Code Ratio

Ratio of test files to source files.

| Range | Level | Score |
|-------|-------|-------|
| 0.8+ | Excellent | 0 |
| 0.5-0.8 | Good | 20 |
| 0.3-0.5 | Moderate | 45 |
| 0.1-0.3 | Poor | 70 |
| 0-0.1 | Critical | 100 |

## Critical Path Coverage

Coverage requirements for critical code paths.

**Minimum Coverage**: 90%

**Critical Patterns**:
- `**/auth/**`
- `**/payment/**`
- `**/security/**`
- `**/api/**`
- `**/core/**`

## Coverage Trends

Track coverage changes over time.

| Metric | Threshold |
|--------|-----------|
| Warning Decrease | 5% drop in 30 days |
| Critical Decrease | 10% drop in 30 days |
| Period | 30 days |

## Uncovered Code Debt

Risk levels for specific uncovered areas:

| Area | Risk Level |
|------|------------|
| Error handlers | High |
| Authentication | Critical |
| Data validation | High |
| Edge cases | Medium |

## Remediation Strategies

### Low Line Coverage

1. Identify uncovered critical paths first
2. Add integration tests for main workflows
3. Use coverage tools to find gaps
4. Focus on business logic over boilerplate

### Low Branch Coverage

1. Review conditional logic without tests
2. Add tests for edge cases
3. Test error handling paths
4. Cover boundary conditions

### Poor Test-to-Code Ratio

1. Establish testing guidelines
2. Require tests for new code
3. Add tests during bug fixes
4. Schedule dedicated test improvement time

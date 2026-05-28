# Debt Scoring

Methodology for scoring and prioritizing technical debt.

## Scoring Dimensions

### Impact Score (1-5)

How much does this debt affect the team/product?

| Score | Level | Description | Examples |
|-------|-------|-------------|----------|
| 5 | Critical | Security risk, data loss, revenue impact | SQL injection, no backups |
| 4 | High | Major feature blocked, significant slowdown | Can't ship feature, 2x dev time |
| 3 | Medium | Development noticeably slower | Extra testing, workarounds |
| 2 | Low | Minor inconvenience | Occasional friction |
| 1 | Minimal | Cosmetic, negligible effect | Code style, naming |

### Effort Score (1-5)

How much work to resolve?

| Score | Level | Time Estimate | Examples |
|-------|-------|---------------|----------|
| 1 | Quick | Hours | Rename variable, add comment |
| 2 | Small | 1-3 days | Extract method, add tests |
| 3 | Medium | 1-2 weeks | Refactor service, update deps |
| 4 | Large | 2-4 weeks | Rewrite module, major migration |
| 5 | Huge | Months | Architecture change, replatform |

### Risk Score (1-5)

What's the risk of the fix causing issues?

| Score | Level | Description |
|-------|-------|-------------|
| 1 | None | Isolated change, well-tested |
| 2 | Low | Limited scope, good test coverage |
| 3 | Medium | Multiple files, some risk |
| 4 | High | Core functionality, wide impact |
| 5 | Critical | Production risk, requires careful rollout |

## Priority Calculation

### Basic Formula

```
Priority Score = Impact × (6 - Effort)
```

This rewards high-impact, low-effort items (quick wins).

| Score Range | Priority | Action |
|-------------|----------|--------|
| 20-25 | P0 | Do immediately |
| 12-19 | P1 | Do this sprint |
| 6-11 | P2 | Do next sprint |
| 1-5 | P3 | Backlog |

### With Risk Adjustment

```
Adjusted Score = (Impact × (6 - Effort)) / Risk
```

Higher risk lowers priority (more careful planning needed).

## Scoring Matrix

### Quick Reference Table

| Impact ↓ / Effort → | 1 (Hours) | 2 (Days) | 3 (Week) | 4 (Weeks) | 5 (Months) |
|---------------------|-----------|----------|----------|-----------|------------|
| 5 (Critical) | **P0** 25 | **P0** 20 | P1 15 | P1 10 | P2 5 |
| 4 (High) | **P0** 20 | P1 16 | P1 12 | P2 8 | P2 4 |
| 3 (Medium) | P1 15 | P1 12 | P2 9 | P2 6 | P3 3 |
| 2 (Low) | P1 10 | P2 8 | P2 6 | P3 4 | P3 2 |
| 1 (Minimal) | P2 5 | P3 4 | P3 3 | P3 2 | P3 1 |

### Quick Wins Quadrant

```
                    LOW EFFORT          HIGH EFFORT
                    ┌───────────────────┬───────────────────┐
    HIGH IMPACT     │   ★ QUICK WINS    │   MAJOR PROJECTS  │
                    │   Do first!       │   Plan carefully  │
                    │   P0/P1           │   P1/P2           │
                    ├───────────────────┼───────────────────┤
    LOW IMPACT      │   FILL-INS        │   AVOID           │
                    │   When convenient │   Question need   │
                    │   P2/P3           │   P3/Never        │
                    └───────────────────┴───────────────────┘
```

## Category-Specific Scoring

### Security Debt

Always score high on impact:

| Vulnerability Type | Minimum Impact | Typical Priority |
|-------------------|----------------|------------------|
| SQL Injection | 5 | P0 |
| XSS | 4 | P0/P1 |
| Auth Bypass | 5 | P0 |
| Sensitive Data Exposure | 4 | P0/P1 |
| Outdated Deps (CVE) | 3-5 | P0-P2 |

### Test Debt

Score based on what's untested:

| Untested Area | Impact | Typical Priority |
|---------------|--------|------------------|
| Payment processing | 5 | P0 |
| Authentication | 4 | P1 |
| Core business logic | 3-4 | P1/P2 |
| UI components | 2 | P2/P3 |
| Admin features | 2 | P3 |

### Documentation Debt

Usually lower priority unless blocking:

| Missing Doc | Impact | Typical Priority |
|-------------|--------|------------------|
| API docs (external) | 3-4 | P1/P2 |
| Onboarding guide | 3 | P2 |
| Architecture docs | 2 | P2/P3 |
| Code comments | 1-2 | P3 |

## Velocity Impact Scoring

Alternative method: score by development velocity impact.

### Daily Impact Estimate

```
Daily Cost = (Developers Affected) × (Minutes Lost/Day) × ($/Minute)
```

Example:
- 5 developers affected
- 30 minutes lost per day each
- $1/minute (loaded cost)
- Daily Cost = 5 × 30 × $1 = $150/day

### ROI Calculation

```
ROI = (Daily Cost × 365) / Resolution Cost

Resolution Cost = Effort (days) × Daily Rate
```

Example:
- Daily Cost: $150
- Resolution: 3 days × $800/day = $2,400
- Annual Savings: $150 × 365 = $54,750
- ROI = $54,750 / $2,400 = **22.8x**

## Team Scoring Session

### Process

1. **Present** each debt item (2 min)
2. **Individual scoring** - everyone scores independently
3. **Reveal** - show all scores
4. **Discuss** - if scores vary by >2, discuss why
5. **Consensus** - agree on final score

### Scoring Card Template

```markdown
## DEBT-XXX: [Title]

### Description
[Brief description]

### Your Scores (1-5)
- Impact: ___
- Effort: ___
- Risk: ___

### Notes
[Any considerations]
```

## Recalibration

Rescore debt periodically:

### When to Rescore

- Every quarter
- After major architecture changes
- When priorities shift
- After partial resolution

### Score Drift Signs

- P2 item blocking features (should be P1)
- P1 item nobody mentions (might be P3)
- Effort estimates were wrong
- Impact changed due to business changes

## Example Scoring

### Example 1: Duplicate Validation

```
Item: Duplicate email validation in 5 controllers
Impact: 2 (Low - occasional bugs, minor slowdown)
Effort: 2 (Days - extract to shared validator)
Risk: 1 (Low - well-tested operation)

Score: 2 × (6-2) / 1 = 8
Priority: P2
```

### Example 2: No Payment Tests

```
Item: Payment processing has 10% test coverage
Impact: 5 (Critical - revenue risk)
Effort: 3 (Week - comprehensive test suite)
Risk: 2 (Low - adding tests, not changing code)

Score: 5 × (6-3) / 2 = 7.5
Priority: P1 (but could argue P0 given criticality)
```

### Example 3: Outdated React

```
Item: React 16 → 18 upgrade needed
Impact: 3 (Medium - missing features, security)
Effort: 4 (Weeks - breaking changes)
Risk: 4 (High - affects whole frontend)

Score: 3 × (6-4) / 4 = 1.5
Priority: P3 (plan carefully, don't rush)
```

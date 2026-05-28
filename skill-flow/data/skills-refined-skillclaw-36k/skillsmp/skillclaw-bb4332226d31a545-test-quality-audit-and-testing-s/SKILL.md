---
name: test-quality-audit-and-testing-strategy
description: Use this skill when you need to conduct a comprehensive audit of your test suite's quality and establish a testing strategy that incorporates risk-based testing and usefulness scoring.
---

# Skill body

## Triggers

- When a review of the test suite is requested
- When test execution times are long
- When flaky tests occur
- When onboarding new team members
- When a test plan is needed
- During overall review of the test suite
- When formulating a testing strategy

## Audit Process

1. List all tests
2. Calculate Usefulness Score
3. Categorize tests
4. Identify candidates for removal
5. Propose improvements

## Usefulness Score Evaluation

### Calculation Formula

```
Score = Impact(1-5) × Probability(1-5)
```

### Evaluation Criteria

| Score | Judgment | Action |
|-------|----------|--------|
| ≥20   | CRITICAL | Must maintain, highest priority for fixing |
| 15-19 | KEEP     | Maintain |
| 10-14 | REVIEW   | Reconsider, consider integration |
| <10   | REMOVE   | Candidate for removal |

### Impact Criteria

| Value | Impact Scope |
|-------|--------------|
| 5     | Money/Security/Data loss |
| 4     | Major function failure |
| 3     | UX degradation |
| 2     | Minor bug |
| 1     | Cosmetic only |

### Probability Criteria

| Value | Frequency of Occurrence |
|-------|-------------------------|
| 5     | Can occur daily |
| 4     | More than once a week |
| 3     | More than once a month |
| 2     | More than once a year |
| 1     | Almost never occurs |

## Audit Checklist

### 1. Business Value Audit

- [ ] Does the test validate business logic?
- [ ] Is it not a framework feature test?
- [ ] Does it directly relate to user value?

### 2. Duplication Audit

- [ ] Are multiple tests verifying the same behavior?
- [ ] Is it written in Unit when covered by E2E?
- [ ] Are there tests that can be integrated?

### 3. Reliability Audit

- [ ] Are there any flaky tests?
- [ ] Are there environment-dependent tests?
- [ ] Are there execution order dependencies?

### 4. Maintainability Audit

- [ ] Is the intent clear from the test name?
- [ ] Is it easy to identify the cause of failure?
- [ ] Is the test data clear?

### 5. Performance Audit

- [ ] Is the execution time within acceptable limits?
- [ ] Are there unnecessary setup/teardown steps?
- [ ] Can it be executed in parallel?

## Deletion Candidates

### Immediate Deletion

| Pattern | Reason |
|---------|--------|
| Framework tests | Responsibility of the framework |
| Getter/Setter tests | No value |
| Constructor tests | No value |
| Mock verification only | Implementation detail |
| Always passing tests | No meaning |

### Consideration for Deletion

| Pattern | Condition |
|---------|-----------|
| Duplicate tests | Covered at a higher level |
| Old tests | Corresponding functionality has been removed |
| Overly complex tests | Maintenance cost > value |

## Required Coverage Thresholds

| Area | Minimum Score |
|------|---------------|
| Money-related | 20+ |
| Security-related | 20+ |
| Authentication/Authorization | 20+ |
| Data persistence | 15+ |

**Threshold not met = Release block**

## Testing Layer Execution Order

```
Database → Backend → Frontend → E2E
```

Each layer must be stable before proceeding to the next.

## Prohibited Actions

- ❌ Adding tests without audit
- ❌ Tests without usefulness scores
- ❌ Leaving candidates for deletion unaddressed
- ❌ Allowing flaky tests
- ❌ Maintaining framework tests

## Quality Gates

| Metric | Threshold |
|--------|-----------|
| Ratio of REMOVE | <5% |
| Flaky rate | 0% |
| Average score | ≥15 |
| Coverage gap | 0 |
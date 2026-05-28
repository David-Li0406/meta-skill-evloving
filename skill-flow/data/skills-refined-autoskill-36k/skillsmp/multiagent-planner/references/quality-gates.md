# Quality Gates

Verification policies organized by risk level and change type.

## Risk Level Assessment

### Low Risk
- Documentation-only changes
- Test-only additions (not modifications)
- Localized bug fixes with existing test coverage
- Style/formatting changes

### Medium Risk
- Feature additions with clear scope
- Refactoring with existing test coverage
- Bug fixes requiring new tests
- Internal API changes

### High Risk
- Security-sensitive changes (auth, payments, data)
- Public API modifications
- Database migrations
- Cross-module refactoring
- Performance-critical paths
- Breaking changes

## Verification Policies by Risk Level

### Low Risk Gates

```
Required:
- [ ] Lint passes
- [ ] Existing tests pass
- [ ] PR/commit follows conventions

Optional:
- [ ] Manual review by one person
```

### Medium Risk Gates

```
Required:
- [ ] Lint passes
- [ ] All existing tests pass
- [ ] New tests added for changed behavior
- [ ] Test coverage maintained or improved
- [ ] Code review completed

Recommended:
- [ ] Integration tests pass
- [ ] No new warnings introduced
```

### High Risk Gates

```
Required:
- [ ] Full test suite passes
- [ ] New tests cover all edge cases
- [ ] Security review completed
- [ ] Performance benchmarks (if perf-critical)
- [ ] Migration tested on staging data
- [ ] Rollback plan documented and tested
- [ ] Two reviewer approvals

Mandatory:
- [ ] Advisory Panel consultation
- [ ] Architect sign-off (if architectural)
```

## Gate Definitions

### Lint Gate
```bash
# Ask Explorer for the lint command, then run:
[project lint command]
# Must exit 0 with no errors
```

### Unit Test Gate
```bash
# Ask Explorer for test command, then run:
[project test command]
# All tests must pass
```

### Integration Test Gate
```bash
# If project has integration tests:
[integration test command]
# All tests must pass
```

### Type Check Gate
```bash
# If project uses static typing:
[typecheck command]  # e.g., tsc --noEmit, mypy, etc.
# Must exit 0
```

### Security Gate

For security-sensitive changes, verify:
1. No hardcoded secrets
2. Input validation present
3. Output encoding for user data
4. Authentication checks in place
5. Authorization verified
6. SQL/NoSQL injection prevention
7. XSS prevention
8. CSRF protection (if applicable)

### Performance Gate

For performance-critical changes:
1. Benchmark before and after
2. No N+1 queries introduced
3. Memory usage stable
4. Response time within SLA
5. No blocking operations in hot paths

## Definition of Done Checklist

### Minimum (All Changes)
- [ ] Code compiles/builds without errors
- [ ] Lint passes
- [ ] Existing tests pass
- [ ] Changes are committed with descriptive message

### Standard (Most Changes)
All of minimum, plus:
- [ ] New tests cover new/changed behavior
- [ ] Documentation updated if needed
- [ ] No TODO comments left (or explicitly tracked)
- [ ] Code review approved

### Comprehensive (High Risk)
All of standard, plus:
- [ ] Security review completed
- [ ] Performance verified
- [ ] Rollback plan in place
- [ ] Monitoring/alerting updated
- [ ] Stakeholder sign-off

## Checkpoint Strategy

For multi-step changes, verify at each checkpoint:

```
Step 1: [action]
├── Checkpoint: [verifiable state]
├── Verify: [command to run]
└── Rollback: [how to undo]

Step 2: [action]
├── Checkpoint: [verifiable state]
├── Verify: [command to run]
└── Rollback: [how to undo]
```

## Failure Handling

If any gate fails:

1. **Stop immediately** - don't proceed to next step
2. **Document the failure** - what failed and why
3. **Assess impact** - is this blocking or can it be addressed?
4. **Create fix plan** - specific steps to resolve
5. **Re-run gates** - after fix is applied

## Continuous Verification

During implementation:
- Run tests after each file modification
- Lint after each logical change
- Typecheck before commits
- Full suite before PR/merge

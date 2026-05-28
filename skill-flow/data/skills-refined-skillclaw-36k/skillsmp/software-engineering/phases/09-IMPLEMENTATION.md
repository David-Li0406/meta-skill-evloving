# Phase 9: Implementation

## Objective

Build the application to pass all tests while following the architecture and interface contracts.

## Step 1: Implementation Order

Determine optimal implementation sequence:

```markdown
### Decision: Implementation Order

**Based on Dependency Graph**:

```
Phase 1: Foundation (No dependencies)
├── Configuration loading
├── Logging setup
└── Database connection

Phase 2: Core Domain (Depends on Foundation)
├── Entity models
├── Business logic
└── Validation rules

Phase 3: Data Layer (Depends on Core Domain)
├── Repositories
├── Migrations
└── Seeds

Phase 4: Service Layer (Depends on Data Layer)
├── Business services
├── External integrations
└── Event handlers

Phase 5: Presentation (Depends on Service Layer)
├── API handlers / CLI commands / UI components
├── Middleware
└── Error handling

Phase 6: Integration (Depends on all above)
├── Wire everything together
├── Configuration injection
└── Entry point
```

**Recommended Approach**:

| Approach | Description | Pros | Cons |
|----------|-------------|------|------|
| **Bottom-Up (Recommended)** | Foundation → Domain → Data → Services → API | Tests pass incrementally, stable foundation | Delayed visible progress |
| Top-Down | API → Services → Data → Domain | Quick visible results | Mocking complexity, unstable |
| Slice-by-Feature | Complete one feature at a time | Feature-complete incrementally | Cross-feature dependencies |

**Implementation Plan**:
[Order based on selected approach]
```

## Step 2: Component Implementation Workflow

For each component, follow this workflow:

```markdown
### Component Implementation: [Component Name]

**1. Review Tests**:
```bash
# Run only this component's tests
npm test -- --grep "[ComponentName]"
# Expected: All FAILING
```

**2. Implement Minimum to Pass First Test**:
```typescript
// Start with simplest implementation
export function componentMethod(input: Input): Output {
  // Minimal implementation
  return expectedOutput;
}
```

**3. Run Tests**:
```bash
npm test -- --grep "[ComponentName]"
# Expected: First test PASSING, others FAILING
```

**4. Iterate**:
- Implement next failing test
- Run tests
- Refactor if needed (keeping tests green)
- Repeat until all tests pass

**5. Verify Coverage**:
```bash
npm test -- --coverage --grep "[ComponentName]"
# Verify coverage meets targets
```

**6. Code Review Checklist**:
- [ ] All tests pass
- [ ] Coverage meets target
- [ ] Follows coding standards
- [ ] No security vulnerabilities
- [ ] Documentation updated
```

## Step 3: Implementation Progress Tracking

```markdown
### Implementation Progress

Copy and update this tracker:

```
Implementation Progress:
- [ ] Phase 1: Foundation
  - [ ] Config loader - [0/3 tests]
  - [ ] Logger setup - [0/2 tests]
  - [ ] DB connection - [0/4 tests]
- [ ] Phase 2: Core Domain
  - [ ] User entity - [0/5 tests]
  - [ ] Resource entity - [0/6 tests]
  - [ ] Validation - [0/8 tests]
- [ ] Phase 3: Data Layer
  - [ ] User repository - [0/7 tests]
  - [ ] Resource repository - [0/9 tests]
- [ ] Phase 4: Services
  - [ ] Auth service - [0/10 tests]
  - [ ] Resource service - [0/12 tests]
- [ ] Phase 5: Presentation
  - [ ] Auth endpoints - [0/6 tests]
  - [ ] Resource endpoints - [0/8 tests]
- [ ] Phase 6: Integration
  - [ ] Wiring - [0/4 tests]
  - [ ] E2E tests - [0/5 tests]
```

**Current Status**:
| Metric | Value |
|--------|-------|
| Total Tests | [N] |
| Passing | [X] |
| Failing | [Y] |
| Coverage | [Z]% |
```

## Step 4: Handling Deviations

When implementation requires changes to design:

```markdown
### Design Deviation: [ID]

**Original Design**:
[What was planned]

**Implementation Reality**:
[What we discovered]

**Proposed Change**:

| Aspect | Before | After | Rationale |
|--------|--------|-------|-----------|
| [Interface] | [Old] | [New] | [Why needed] |
| [Architecture] | [Old] | [New] | [Why needed] |

**Impact Analysis**:
- Tests affected: [List]
- Contracts affected: [List]
- User impact: [Description]

**Recommendation**: [Proceed with change / Rework implementation / Discuss with user]

---

**Do you approve this deviation?**
```

## Step 5: Quality Gates

At each implementation phase:

```markdown
### Quality Gate: [Phase Name]

**Tests**:
- [ ] All unit tests for phase pass
- [ ] Integration tests (if applicable) pass
- [ ] No regression in existing tests

**Coverage**:
- [ ] Line coverage: [X]% (target: [Y]%)
- [ ] Branch coverage: [X]% (target: [Y]%)

**Code Quality**:
- [ ] Linting passes (0 errors, 0 warnings)
- [ ] No TypeScript/type errors
- [ ] No security warnings

**Performance** (if applicable):
- [ ] No obvious N+1 queries
- [ ] Response times within targets

**Documentation**:
- [ ] Code comments for complex logic
- [ ] API documentation updated
- [ ] README updated if needed

**Verdict**: [PASS / FAIL - reason]
```

## Step 6: Debugging Guidelines

When tests fail unexpectedly:

```markdown
### Debugging Checklist

**1. Understand the Failure**:
```bash
# Run single test with verbose output
npm test -- --verbose "[test name]"
```

**2. Isolate the Issue**:
- Is it a test bug or implementation bug?
- Does it fail consistently or intermittently?
- Does it fail in isolation or only with other tests?

**3. Common Issues**:

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Works locally, fails in CI | Environment difference | Check env vars, versions |
| Intermittent failure | Race condition | Add proper async handling |
| Test passes alone, fails together | State leakage | Reset state in beforeEach |
| Type error at runtime | Missing validation | Add input validation |

**4. Fix Strategy**:
- Fix the root cause, not symptoms
- Add test for the bug before fixing
- Verify fix doesn't break other tests
```

## Step 7: Implementation Review Points

Present progress at key milestones:

```markdown
### Implementation Review: [Milestone]

**Completed**:
| Component | Tests | Status |
|-----------|-------|--------|
| [Component A] | 10/10 | ✅ Complete |
| [Component B] | 8/8 | ✅ Complete |

**In Progress**:
| Component | Tests | Status |
|-----------|-------|--------|
| [Component C] | 5/12 | 🔄 In Progress |

**Blocked/Issues**:
| Issue | Impact | Proposed Resolution |
|-------|--------|---------------------|
| [Issue 1] | [Impact] | [Resolution] |

**Metrics**:
```
Tests: 45/67 passing (67%)
Coverage: 72%
Build: ✅ Passing
Lint: ✅ No issues
```

**Next Steps**:
1. [Next component to implement]
2. [Expected blockers]

---

**Continue with implementation?**
```

## Phase 9 Approval Gate

```markdown
## Phase 9 Summary: Implementation

### Implementation Status
```
All Tests: PASSING ✅
Total: [N] tests
Coverage: [X]%
Build: ✅ Success
```

### Components Implemented
| Component | Tests | Coverage | Status |
|-----------|-------|----------|--------|
| [Component A] | [X/X] | [Y]% | ✅ |
| [Component B] | [X/X] | [Y]% | ✅ |

### Deviations from Design
| Deviation | Approved | Reason |
|-----------|----------|--------|
| [Deviation 1] | Yes/No | [Reason] |

### Known Issues
| Issue | Severity | Planned Resolution |
|-------|----------|-------------------|
| [Issue 1] | [H/M/L] | [Plan] |

### Performance Baseline
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Response Time (p95) | [X]ms | [Y]ms | ✅/❌ |
| Memory Usage | [X]MB | [Y]MB | ✅/❌ |

### Ready for Production?
- [ ] All tests pass
- [ ] Coverage meets targets
- [ ] No critical security issues
- [ ] Documentation complete
- [ ] Performance acceptable

---

**Do you approve Phase 9? Ready for Simulation Testing (if applicable)?**
```

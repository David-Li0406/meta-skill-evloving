# Planning Patterns

**Purpose**: Reusable strategies for different types of planning scenarios.

---

## Pattern 1: Feature Planning

**Characteristics**:
- Multiple requirements
- Cross-cutting changes (database, backend, frontend)
- User-facing functionality

**Strategy**:
1. Start with schema changes (database layer)
2. Build up backend logic
3. Add user interface
4. End with end-to-end tests

**Task Organization** (Article VII):
```
Phase 1: Setup (infrastructure)
Phase 2: Foundational (blocking prerequisites)
Phase 3: User Story P1 (MVP, independently testable)
Phase 4: User Story P2 (enhancements)
Phase 5: User Story P3 (nice-to-have)
Final Phase: Polish & Integration
```

**Example Breakdown**:
```
Feature: OAuth Login

Tasks:
- T1: Add google_id to users table (DB)
- T2: Implement OAuth flow (backend)
- T3: Create OAuth callback handler (backend)
- T4: Add "Login with Google" button (frontend)
- T5: Implement session management (backend)
- T6: E2E test OAuth flow (testing)

Organization:
- P1 (MVP): T1, T2, T3, T4 (basic OAuth login)
- P2 (Enhancement): T5 (session management)
- P3 (Nice-to-have): Account linking, profile sync
```

**Common Pitfalls**:
- ❌ "Implement all models" phase (layer-first, not story-first)
- ❌ "Complete backend before frontend" (big-bang integration)
- ✓ Organize by user story priority (P1, P2, P3)

---

## Pattern 2: Refactor Planning

**Characteristics**:
- Improve existing code
- Must maintain behavior
- No new features

**Strategy**:
1. Understand current implementation via intelligence queries
2. Create comprehensive tests FIRST (lock in behavior)
3. Make small, incremental refactors
4. Verify no regressions at each step

**Task Organization**:
```
Phase 1: Intelligence Gathering
- T1: Query existing code structure
- T2: Map current behavior

Phase 2: Test Creation
- T3: Write tests for existing behavior
- T4: Verify tests pass on current code

Phase 3: Incremental Refactoring
- T5: Extract function X
- T6: Rename variable Y
- T7: Consolidate duplicate code Z
(Each with regression tests)

Phase 4: Verification
- T8: Run full test suite
- T9: Performance comparison
```

**Example Breakdown**:
```
Refactor: Payment Processing Module

Tasks:
- T1: Intel query payment processing files
- T2: Analyze current payment flow (CoD^Σ trace)
- T3: Write characterization tests
- T4: Extract discount calculation logic
- T5: Consolidate tax calculation code
- T6: Rename variables for clarity
- T7: Verify performance unchanged
```

**Key Principle**: **Tests FIRST, then refactor** (Article III)

**Common Pitfalls**:
- ❌ Refactoring without tests (can't verify no regressions)
- ❌ Big-bang refactor (high risk, hard to debug)
- ✓ Small incremental changes with test verification

---

## Pattern 3: Migration Planning

**Characteristics**:
- Large-scale change (database, framework, language)
- Must support both old and new systems during transition
- Gradual rollout required

**Strategy**:
1. Run both old and new systems in parallel
2. Migrate incrementally (not all at once)
3. Use feature flags for gradual rollout
4. Only deprecate old system after 100% migration complete

**Task Organization**:
```
Phase 1: Parallel System Setup
- T1: Setup new system alongside old
- T2: Configure routing/proxy to both systems

Phase 2: Dual-Write Implementation
- T3: Write to both old and new systems
- T4: Verify consistency between systems

Phase 3: Gradual Read Migration
- T5: Route 10% reads to new system
- T6: Route 50% reads to new system
- T7: Route 100% reads to new system

Phase 4: Cleanup
- T8: Remove old system dependencies
- T9: Deprecate old APIs
- T10: Archive old code
```

**Example Breakdown**:
```
Migration: PostgreSQL to MongoDB

Tasks:
- T1: Setup MongoDB cluster
- T2: Create dual-write logic (write to both DBs)
- T3: Verify data consistency script
- T4: Route 10% reads to MongoDB
- T5: Monitor error rates, rollback if needed
- T6: Route 50% reads to MongoDB
- T7: Route 100% reads to MongoDB
- T8: Stop writes to PostgreSQL
- T9: Archive PostgreSQL data
- T10: Deprecate PostgreSQL connection
```

**Feature Flag Strategy**:
```javascript
if (isFeatureEnabled('mongodb-reads')) {
  return readFromMongoDB()
} else {
  return readFromPostgreSQL()
}
```

**Common Pitfalls**:
- ❌ Big-bang migration (all at once, high risk)
- ❌ No rollback plan (stuck if issues found)
- ✓ Incremental rollout with monitoring at each step

---

## Pattern 4: Bug Fix Planning

**Characteristics**:
- Fix existing broken behavior
- Root cause already identified (from debug-issues skill)
- Regression tests required

**Strategy**:
1. Reproduce bug with failing test
2. Implement minimal fix
3. Verify fix passes test
4. Add regression tests for edge cases

**Task Organization**:
```
Phase 1: Test Creation
- T1: Write failing test that reproduces bug

Phase 2: Fix Implementation
- T2: Implement minimal fix

Phase 3: Regression Prevention
- T3: Add tests for related edge cases
- T4: Document fix and prevention strategy
```

**Example Breakdown**:
```
Bug: Division by zero in discount calculation

Tasks:
- T1: Write test that triggers division by zero
- T2: Add validation to prevent zero division
- T3: Add tests for 0%, 50%, 100% discount cases
- T4: Update documentation with edge case handling
```

**Common Pitfalls**:
- ❌ Fixing bug without test (might reintroduce later)
- ❌ Over-engineering fix (introduce new bugs)
- ✓ Minimal fix with comprehensive tests

---

## Pattern Selection Guide

| Scenario | Pattern | Why |
|----------|---------|-----|
| New feature, multiple user stories | Feature Planning | Story-first organization |
| Improving existing code quality | Refactor Planning | Behavior preservation critical |
| Moving to new system/tech | Migration Planning | Risk mitigation via gradual rollout |
| Fixing specific bug | Bug Fix Planning | Test-first, minimal fix |

---

## Common Across All Patterns

**Intelligence-First** (Article I):
- Always query project-intel.mjs before planning
- Save evidence to /tmp/*.json
- Reference findings in plan (file:line)

**Test-First** (Article III):
- Define ACs before implementation
- Minimum 2 testable ACs per task
- Run tests before marking task complete

**Evidence-Based** (Article II):
- CoD^Σ traces with file:line references
- No unsupported claims
- Save query outputs for audit

**Template-Driven** (Article V):
- Use @.claude/templates/plan.md
- Consistent format across all plans
- Required sections present

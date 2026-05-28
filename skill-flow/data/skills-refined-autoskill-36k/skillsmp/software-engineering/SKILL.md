---
name: software-engineering
description: Implements software from requirements and design specifications. Covers code scaffolding, test-driven development, implementation, and simulation testing with iterative feedback loops. Use after product-development skill or when you have existing requirements/designs to implement.
---

# Software Engineering Workflow

Implements software products from requirements and design artifacts with iterative development loops.

## Prerequisites

Before starting, ensure you have:
- Product requirements (user stories, acceptance criteria)
- Technical requirements (NFRs, constraints)
- Architecture design (component diagrams, data models)
- Interface contracts (API specs, CLI syntax)

If missing, run `product-development` skill first.

## Role Boundaries

| Activity | Claude | User |
|----------|--------|------|
| Scaffold code | ✅ Creates structure, stubs | Reviews structure |
| Write tests | ✅ Implements test cases | Reviews coverage |
| Implement code | ✅ Writes implementation | Reviews, approves |
| Debug failures | ✅ Analyzes, proposes fixes | Confirms direction |
| Approval gates | ✅ Shows status, asks | Approves / requests changes |

## Iteration Limits

| Loop | Max Iterations | Escalation |
|------|----------------|------------|
| Test coverage review | 3 | "Coverage target may be unrealistic" |
| Red-Green-Refactor | 5 per component | "Component may need redesign" |
| Fix-Retest (simulation) | 3 | "Architecture may have fundamental issues" |

**Escalation options**: (A) Accept current state, (B) Reduce scope, (C) Return to `product-development` for redesign

## Artifacts Location

Implementation outputs go to project root (alongside planning):

```
project/
├── planning/           # From product-development
├── src/                # Phase 1: scaffolding
│   └── {modules}/
├── tests/              # Phase 2: test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── flake.nix           # From nix-devenv
├── Containerfile       # From podman-deploy
├── .github/workflows/  # From github-actions-ci
└── docs/               # From sphinx-docs
```

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOFTWARE ENGINEERING                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: Code Scaffolding ──────────────────→ User Approval    │
│                                                     │           │
│                                          ┌──────────┘           │
│                                          ▼                      │
│  Phase 2: Test Development ←────── Review Loop ──→ User Approval│
│           │                              ▲                      │
│           │                              │                      │
│           ▼                              │                      │
│  Phase 3: Implementation ───────────────────────→ User Approval │
│           │         ▲                                           │
│           │         │                                           │
│           └─── Red/Green/Refactor Loop                          │
│                                                                 │
│  Phase 4: Simulation Testing (if needed) ────→ User Approval    │
│           │         ▲                                           │
│           │         │                                           │
│           └─── Fix/Retest Loop                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Companion Skills

| Task | Skill | When |
|------|-------|------|
| Create diagrams | `diagrams-kroki` | Architecture visualization |
| Setup environment | `nix-devenv` | Before scaffolding |
| Container builds | `podman-deploy` | Deployment prep |
| CI/CD pipelines | `github-actions-ci` | After implementation |
| Documentation | `sphinx-docs` | Throughout |
| **Complexity scoring** | `dynamic-tasks` | For iteration planning |

---

## Phase 1: Code Scaffolding

**Goal**: Create project structure matching architecture design.

### Checklist

```
Scaffolding:
- [ ] Project directory structure created
- [ ] Module/package stubs with signatures
- [ ] Configuration files (env, build, lint)
- [ ] Dependency management setup
- [ ] Development environment working
```

### Activities

1. **Create directory structure** matching component diagram
2. **Stub out modules** with interfaces (no implementation)
3. **Setup build tooling** (Makefile, justfile, package.json)
4. **Configure linting/formatting** rules
5. **Verify environment** builds without errors

### Approval Gate

```markdown
## Phase 1 Complete: Code Scaffolding

**Structure Created**:
- [X] /cmd/app/main.go
- [X] /internal/service/...
- [X] /pkg/api/...

**Build Status**: ✅ Compiles
**Lint Status**: ✅ Passes

**Do you approve? Any structure changes needed?**
```

---

## Phase 2: Test Development

**Goal**: Write tests before implementation (TDD).

### Test Pyramid

```
        ╱╲
       ╱  ╲         E2E Tests (few)
      ╱────╲        - User journey validation
     ╱      ╲
    ╱────────╲      Integration Tests (some)
   ╱          ╲     - API contracts, DB interactions
  ╱────────────╲
 ╱              ╲   Unit Tests (many)
╱────────────────╲  - Business logic, edge cases
```

### Review Loop

```
┌─────────────────────────────────────────┐
│           TEST REVIEW LOOP              │
├─────────────────────────────────────────┤
│                                         │
│  Write Tests ──→ Review Coverage        │
│       ▲              │                  │
│       │              ▼                  │
│       │         Gaps Found?             │
│       │          ╱      ╲               │
│       │        Yes       No             │
│       │        ╱          ╲             │
│       └───────╱            ╲───→ Done   │
│                                         │
└─────────────────────────────────────────┘
```

### Test Categories

| Category | Tests For | Coverage Target |
|----------|-----------|-----------------|
| Unit | Business logic, utilities | >80% |
| Integration | APIs, database, services | Key paths |
| Contract | API request/response | All endpoints |
| E2E | User flows | Critical paths |

### Checklist

```
Test Development:
- [ ] Unit tests for each component
- [ ] Integration tests for interfaces
- [ ] Contract tests for APIs
- [ ] E2E tests for critical user flows
- [ ] All tests failing (red) - not implemented yet
- [ ] Test coverage report generated
```

### Approval Gate

```markdown
## Phase 2 Complete: Test Development

**Test Summary**:
| Type | Count | Status |
|------|-------|--------|
| Unit | X | 🔴 Failing (expected) |
| Integration | X | 🔴 Failing (expected) |
| E2E | X | 🔴 Failing (expected) |

**Coverage Targets**:
- Unit: X% target
- Critical paths: All covered

**Do you approve? Any test cases missing?**
```

---

## Phase 3: Implementation

**Goal**: Make all tests pass with clean code.

### Red-Green-Refactor Loop

```
┌─────────────────────────────────────────┐
│       RED-GREEN-REFACTOR LOOP           │
├─────────────────────────────────────────┤
│                                         │
│    ┌──────────────────────────────┐     │
│    │                              │     │
│    ▼                              │     │
│  RED ────→ GREEN ────→ REFACTOR ─┘     │
│  (test     (make it    (make it         │
│  fails)    pass)       clean)           │
│                                         │
│  Repeat for each component              │
│                                         │
└─────────────────────────────────────────┘
```

### Implementation Order

1. **Core domain logic** (no dependencies)
2. **Data layer** (repositories, models)
3. **Service layer** (business operations)
4. **API/Interface layer** (handlers, CLI)
5. **Integration points** (external services)

### Per-Component Checklist

```
Component: [Name]
- [ ] Tests exist and are red
- [ ] Implementation complete
- [ ] Tests green
- [ ] Code reviewed for:
    - [ ] No hardcoded values
    - [ ] Error handling
    - [ ] Logging
    - [ ] No security issues
- [ ] Refactored for clarity
```

### Iteration Pattern

For each component:

```markdown
### Implementing: [Component Name]

**Current Status**: 🔴 X tests failing

**Implementation**:
[Code changes here]

**After Implementation**: 🟢 All tests passing

**Refactoring needed?**
| Issue | Action |
|-------|--------|
| [Issue] | [Refactor] |

**Ready to proceed to next component?**
```

### Approval Gate

```markdown
## Phase 3 Progress: Implementation

**Component Status**:
| Component | Tests | Status |
|-----------|-------|--------|
| Domain | 15/15 | 🟢 |
| Repository | 8/8 | 🟢 |
| Service | 12/12 | 🟢 |
| API | 10/10 | 🟡 In Progress |

**Overall**: 35/45 tests passing (78%)

**Continue with next component?**
```

---

## Phase 4: Simulation Testing

**Goal**: Validate system under realistic conditions.

### When Required

- [ ] Distributed system with multiple services
- [ ] High-throughput requirements (>100 req/s)
- [ ] Complex state machines
- [ ] Critical failure handling needed
- [ ] External dependency interactions

If none apply: Skip with justification.

### Fix-Retest Loop

```
┌─────────────────────────────────────────┐
│          FIX-RETEST LOOP                │
├─────────────────────────────────────────┤
│                                         │
│  Run Simulation ──→ Issues Found?       │
│       ▲                  │              │
│       │              Yes │ No           │
│       │                  ▼  ╲           │
│       │             Fix Issues ╲        │
│       │                  │      ╲       │
│       └──────────────────┘       → Done │
│                                         │
└─────────────────────────────────────────┘
```

### Test Types

| Type | Purpose | Tools |
|------|---------|-------|
| Load | Throughput limits | k6, Artillery |
| Chaos | Failure handling | toxiproxy, scripts |
| State | Complex transitions | Custom harness |
| Soak | Memory leaks, degradation | k6 (long run) |

### Checklist

```
Simulation Testing:
- [ ] Load test baseline established
- [ ] Peak load tested
- [ ] Failure scenarios validated
- [ ] Recovery verified
- [ ] Performance baseline documented
```

### Approval Gate

```markdown
## Phase 4 Complete: Simulation Testing

**Results Summary**:
| Test | Target | Actual | Status |
|------|--------|--------|--------|
| Max throughput | >100 req/s | 150 req/s | ✅ |
| p95 latency | <200ms | 180ms | ✅ |
| Recovery time | <30s | 25s | ✅ |

**Issues Found & Fixed**:
| Issue | Resolution |
|-------|------------|
| [Issue] | [Fix] |

**Production Ready?**
```

---

## Completion

```markdown
## Software Engineering Complete

**Final Status**:
- [ ] All code scaffolded
- [ ] All tests written and passing
- [ ] All components implemented
- [ ] Simulation testing complete (or skipped with justification)
- [ ] Documentation updated
- [ ] Ready for deployment

**Artifacts Produced**:
- Source code in repository
- Test suite (X tests)
- CI pipeline configured
- Documentation generated

**Next Steps**:
- Deploy to staging (use `podman-deploy` skill)
- Setup CI/CD (use `github-actions-ci` skill)
```

---

## Interaction Style

1. **Iterate**: Use loops, don't assume first attempt is final
2. **Test First**: Always write tests before implementation
3. **Small Steps**: One component at a time
4. **Verify Often**: Run tests after each change
5. **Approval Gates**: Wait for user approval between phases

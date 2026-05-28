# Implementation Skill

## Philosophy

Good code is not written once and forgotten. It is systematically crafted through disciplined workflows that build quality in from the start, not bolt it on at the end.

This skill embodies a philosophy of **contract-first, test-driven, systematically validated** implementation.

## Core Beliefs

### 1. Contracts Before Code

**The Problem:** Frontend and backend teams implement their understanding of the API, then discover mismatches during integration. Field names differ (snake_case vs camelCase), types diverge, validation rules conflict. Integration becomes debugging sessions.

**The Solution:** DTOs are the contract. Define them from the specification, implement them identically on both sides, validate synchronization BEFORE writing any business logic. Frontend builds UI with correct types. Backend implements logic with correct types. Integration is assembly, not discovery.

### 2. Validation Gates, Not Hope

**The Problem:** "It works on my machine." Code passes informal testing, ships, breaks in production. Linting violations, type errors, missing test coverage discovered too late.

**The Solution:** Systematic validation gates that must pass before work is considered complete. Linting catches style issues. Type checking catches type errors. Tests catch logic bugs. Gates are cheap early, expensive later.

### 3. Standards Enable Speed

**The Problem:** Every file formatted differently, every error handled differently, every pattern implemented differently. Reviewers spend time on style, not substance. Newcomers guess at conventions.

**The Solution:** Documented coding standards applied consistently. Formatters enforce style. Patterns reduce cognitive load. Reviews focus on logic, not formatting. Standards are scaffolding, not constraints.

### 4. Error Handling is Feature Work

**The Problem:** Happy path implemented, error cases ignored. Production failures surface in logs and user complaints. Error messages are generic or expose internals.

**The Solution:** Error handling is first-class implementation work. Expected errors return clear messages. Unexpected errors are logged with context. Users see helpful feedback, not stack traces.

### 5. Tests Are Proof, Not Afterthought

**The Problem:** "We'll add tests later." Later never comes. Tests written after code verify what exists, not what's required. Bugs slip through.

**The Solution:** Test-driven development when appropriate. Tests written first force design decisions. Watching tests fail proves they work. Passing tests enable confident refactoring.

## Implementation Discipline

### Phase 1: Contract Definition (If Applicable)

Before writing business logic:

1. **Extract DTO requirements** from design specification
2. **Implement DTOs/interfaces** exactly matching specification
3. **Create contract validation tests** (structure, not behavior)
4. **Synchronize with other team** (backend ↔ frontend)
5. **Validate contracts pass** before proceeding

**Time Investment:** 30-45 minutes
**Prevents:** Days of integration debugging

### Phase 2: Implementation

With validated contracts:

1. **Implement function signatures** (types defined, logic stubbed)
2. **Write tests** (TDD when appropriate)
3. **Implement business logic** incrementally
4. **Handle errors** systematically
5. **Follow coding standards** consistently

**Focus:** Small, testable increments

### Phase 3: Validation

Before considering work complete:

1. **Lint and format** - Style consistency
2. **Type check** - Type safety verified
3. **Run tests** - Logic correctness proven
4. **Integration test** - Components work together
5. **Manual verification** - Key scenarios validated

**Gates Failed?** Fix immediately, don't defer.

### Phase 4: Documentation

Capture implementation decisions:

1. **Implementation notes** - What was built, how it works
2. **Outstanding TODOs** - What's deferred, why
3. **Update feature docs** - README, API docs, architecture notes

**Future You** will thank Present You.

## Why This Works

### Prevents Common Failures

| Failure Mode | Prevention Mechanism |
|--------------|---------------------|
| Frontend/backend DTO mismatch | Contract-first discipline, synchronization |
| Integration bugs | Contract tests, validation gates |
| Runtime type errors | Type checking gate, strict typing |
| Production failures | Comprehensive error handling, integration tests |
| Inconsistent code style | Linting gate, coding standards |
| Missing test coverage | Testing requirements, validation gates |
| Regression bugs | Automated test suite, continuous validation |

### Enables Team Velocity

- **Parallel development** - Frontend and backend work simultaneously on validated contracts
- **Confident refactoring** - Tests catch breaks immediately
- **Faster reviews** - Standards eliminate style debates
- **Easier onboarding** - Patterns and workflows documented
- **Reduced debugging** - Validation gates catch issues early

### Builds Maintainable Systems

- **Predictable structure** - Consistent patterns across codebase
- **Clear error handling** - Failures are informative
- **Comprehensive tests** - Safe to modify
- **Living documentation** - Tests show intended behavior

## When to Deviate

This discipline is designed for production code. Consider deviations for:

- **Prototypes** - Exploring ideas, will be discarded
- **Generated code** - Tooling produces consistent output
- **Configuration** - Declarative, not algorithmic
- **Urgent hotfixes** - Under time pressure (but add tests immediately after)

**Always discuss deviations with your team.** Cutting corners has costs.

## Integration with Development Process

### Task-Driven Development

When following a Task (formerly PRP):

1. Read task completely
2. Check dependencies
3. **Start task:** `shark task start <task-id>`
4. Review context documents
5. Select implementation workflow
6. Follow blueprint step-by-step
7. Run validation gates per task
8. **Complete task:** `shark task complete <task-id>`

Tasks provide the "what" and "why". This skill provides the "how".

The shark CLI automatically:
- Updates task status in the database
- Tracks implementation progress
- Provides visibility to the team
- Enables accurate reporting

### Agile/Sprint Development

Within sprint work:

1. Review user story/ticket
2. Read design documentation
3. Select implementation workflow
4. Follow contract-first discipline
5. Implement incrementally
6. Pass validation gates
7. Mark story complete

This skill ensures quality regardless of project methodology.

## Measuring Success

Implementation skill is working when:

- Integration sessions are brief assembly, not debugging
- Production bugs are rare, not routine
- Code reviews focus on design, not style
- New team members onboard quickly
- Refactoring is safe and frequent
- Confidence in deployments is high

## Getting Started

1. **Read SKILL.md** - Understand workflow selection
2. **Read context/contract-first.md** - Understand contract discipline (critical!)
3. **Read context/validation-gates.md** - Understand quality gates
4. **Select a workflow** - Based on what you're implementing
5. **Follow the workflow** - Step by step
6. **Pass the gates** - Before considering work complete

---

**Implementation is not coding. Implementation is systematically building quality into code through disciplined workflows.**

Welcome to the implementation skill. Let's build something excellent.

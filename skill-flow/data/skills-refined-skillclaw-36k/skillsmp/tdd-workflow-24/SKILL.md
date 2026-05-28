---
name: tdd-workflow
description: Complete Test-Driven Development workflow coordinating RED → GREEN → REFACTOR → COMMIT cycle with requirement traceability. Use this when implementing a requirement (REQ-*) or adding new functionality.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# tdd-workflow

**Skill Type**: Orchestrator (TDD Workflow)
**Purpose**: Coordinate complete TDD cycle with requirement traceability
**Prerequisites**:
- Work unit with REQ-* key (e.g., "Implement <REQ-ID>")
- Requirement details available

---

## Agent Instructions

You are orchestrating the complete **Test-Driven Development (TDD)** workflow.

Your goal is to implement a requirement using the **RED → GREEN → REFACTOR → COMMIT** cycle while maintaining requirement traceability.

---

## Workflow

### Phase 0: Prerequisites Check

**Before starting TDD, verify**:
1. ✅ Requirement key exists (REQ-F-*, REQ-NFR-*, REQ-DATA-*, REQ-BR-*)
2. ✅ Requirement details available (what to implement)
3. ✅ Working directory is a git repository
4. ✅ No uncommitted changes (clean working tree)

**If prerequisites missing**:
- No REQ-* key → Invoke `requirement-extraction` skill (from requirements-skills plugin)
- No requirement details → Ask user for clarification
- Not a git repo → Ask user if they want to initialize git
- Uncommitted changes → Ask user if they want to commit or stash

---

### Phase 1: RED (Write Failing Tests)

**Invoke**: `red-phase` skill

**Purpose**: Write tests that fail because the code doesn't exist yet

**What red-phase does**:
- Creates test file (e.g., `test_user_login.py`)
- Writes test functions for the requirement
- Tags tests with REQ-* key in comments
- Runs tests → expects FAILURE (RED)
- Commits: "RED: Add tests for REQ-*"

**Success Criteria**: Tests exist and FAIL

---

### Phase 2: GREEN (Make Tests Pass)

**Invoke**: `green-phase` skill

**Purpose**: Write minimal code to make tests pass

**What green-phase does**:
- Creates implementation file (e.g., `auth_service.py`)
- Implements minimal code to pass tests
- Tags code with REQ-* key in comments
- Runs tests → expects SUCCESS (GREEN)
- Commits: "GREEN: Implement REQ-*"

**Success Criteria**: Tests PASS

---

### Phase 3: REFACTOR (Improve Quality + Eliminate Tech Debt)

**Invoke**: `refactor-phase` skill

**Purpose**: Improve code quality and eliminate technical debt (Principle #6)

**What refactor-phase does**:
- Improves code quality (type hints, docstrings, naming)
- **Deletes** unused imports
- **Removes** dead code (functions with zero callers)
- **Deletes** commented-out code
- **Simplifies** over-complex logic (cyclomatic complexity > 10)
- **Removes** code duplication
- Runs tests → expects STILL PASSING
- Commits: "REFACTOR: Clean up REQ-*"

**Success Criteria**: Tests still PASS, tech debt = 0

---

### Phase 4: COMMIT (Final Commit with REQ-* Tag)

**Invoke**: `commit-with-req-tag` skill

**Purpose**: Create final commit with requirement traceability

**What commit-with-req-tag does**:
- Squashes RED, GREEN, REFACTOR commits (optional)
- Creates final commit message:
  ```
  feat: Add user login (<REQ-ID>)

  Implements user authentication with email and password.

  Business Rules:
  - BR-001: Email validation
  - BR-002: Password minimum 12 characters

  Tests: 5 tests, 100% coverage
  ```
- Tags commit with REQ-* key

**Success Criteria**: Final commit created with REQ-* traceability

---

## Output Format

When you complete the TDD workflow, show:

```
[TDD Workflow: <REQ-ID>]

✅ Phase 0: Prerequisites
  ✓ Requirement: <REQ-ID> (User login)
  ✓ Git repository: initialized
  ✓ Working tree: clean

✅ Phase 1: RED (Write Failing Tests)
  ✓ Created: test_user_login.py (5 tests)
  ✓ Tests FAILED as expected ✓
  ✓ Commit: RED: Add tests for <REQ-ID>

✅ Phase 2: GREEN (Make Tests Pass)
  ✓ Created: auth_service.py
  ✓ Implemented: login() function
  ✓ Tests PASSED ✓
  ✓ Commit: GREEN: Implement <REQ-ID>

✅ Phase 3: REFACTOR (Improve Quality + Eliminate Tech Debt)
  Code Quality Improvements:
    ✓ Added type hints to 3 functions
    ✓ Added docstrings to 2 public methods
    ✓ Improved variable names (2 changes)

  Tech Debt Pruning:
    ✓ Deleted 2 unused imports
    ✓ Removed 1 dead function (8 lines)
    ✓ Simplified validation logic (complexity 12 → 6)

  ✓ Tests still PASSING ✓
  ✓ Commit: REFACTOR: Clean up <REQ-ID>

✅ Phase 4: COMMIT (Final Commit)
  ✓ Final commit: feat: Add user login (<REQ-ID>)

🎉 TDD Workflow Complete!
  Files: 2 files (auth_service.py, test_user_login.py)
  Tests: 5 tests, 100% coverage
  Commits: 4 commits (RED, GREEN, REFACTOR, final)
  Traceability: <REQ-ID> → commit abc123
```

---

## Homeostasis Behavior

**If prerequisites not met**:
1. **Detect**: Missing REQ-* key
2. **Signal**: "Need requirement extraction first"
3. **Claude invokes**: `requirement-extraction` skill (from requirements-skills plugin)
4. **Retry**: tdd-workflow with new REQ-*

**If tests fail in GREEN phase**:
1. **Detect**: Tests still failing after implementation
2. **Signal**: "Implementation incomplete"
3. **Claude**: Fix implementation and retry
4. **Do NOT proceed to REFACTOR** until tests pass

**If tech debt detected in REFACTOR phase**:
1. **Detect**: Unused code, complexity > 10, etc.
2. **Signal**: "Tech debt detected"
3. **Claude invokes**: `prune-unused-code`, `simplify-complex-code` (actuator skills)
4. **Verify**: Tech debt eliminated before commit

---

## Prerequisites Check

Before invoking this skill, ensure:
1. ✅ Requirement key (REQ-*) exists
2. ✅ Requirement details available
3. ✅ Git repository initialized
4. ✅ Clean working tree

If prerequisites not met:
- Missing REQ-* → Invoke `requirement-extraction` skill
- No git → Ask user to initialize
- Dirty working tree → Ask user to commit or stash

---

## Skills Used

This orchestrator skill invokes:
1. `red-phase` - Write failing tests
2. `green-phase` - Implement code to pass tests
3. `refactor-phase` - Improve quality and eliminate tech debt
4. `commit-with-req-tag` - Create final commit with traceability
5. `detect-unused-code` - (via refactor-phase) Detect tech debt
6. `prune-unused-code` - (via refactor-phase) Eliminate tech debt
7. `detect-complexity` - (via refactor-phase) Detect over-complex code
8. `simplify-complex-code` - (via refactor-phase) Simplify complex code

---

## Configuration

This skill respects configuration in `.claude/plugins.yml`:

```yaml
plugins:
  - name: "@aisdlc/code-skills"
    config:
      tdd:
        minimum_coverage: 80          # Fail if coverage < 80%
        enforce_red_green_refactor: true  # Enforce phase order
        allow_skip_tests: false       # Block if user tries to skip tests
        squash_commits: false         # Keep RED/GREEN/REFACTOR commits separate
```

---

## Next Steps

After TDD workflow completes:
1. Review final commit
2. Push to remote (if desired)
3. Move to next requirement (invoke `tdd-workflow` for next REQ-*)

---

## Notes

**Why TDD workflow?**
- Tests first = clear specification before coding
- RED phase = verify tests can fail (avoid false positives)
- GREEN phase = minimal implementation (no over-engineering)
- REFACTOR phase = quality + tech debt elimination (Principle #6)
- COMMIT phase = requirement traceability (forward + backward)

**Homeostasis Goal**:
```yaml
desired_state:
  tests_written_first: true
  tests_passing: true
  tech_debt: 0
  requirement_traceability: complete
```

**"Excellence or nothing"** 🔥

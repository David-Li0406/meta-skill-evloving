---
name: add-test-coverage
description: Analyze git HEAD commit changes and implement comprehensive test coverage. Supports unit tests, integration tests, and E2E tests. Automatically detects language and testing frameworks from the repository.
license: MIT
compatibility:
  - vcs:git
  - runtime:any
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(git:diff)
  - Bash(git:log)
  - Bash(git:show)
  - Bash(git:status)
  - Bash(git:rev-parse)
metadata:
  author: thoreinstein
  version: 1.0.0
---

# Add Test Coverage

Analyze the most recent commit (HEAD) and implement all tests required to cover new and modified code.

## When to Use This Skill

- After completing a feature or fix, to ensure adequate test coverage before merge
- When a commit introduces new functions, methods, or API endpoints
- When modifying existing behavior that may not have sufficient tests
- During code review when test coverage gaps are identified

## Workflow

### Phase 1: Change Analysis

1. Identify changes in the latest commit:
   - Diff HEAD against its parent (HEAD~1), or against the appropriate base branch if more accurate
2. Classify each changed file by type based on file extensions and project structure:
   - Backend code (e.g., `.go`, `.py`, `.java`, `.rb`)
   - Frontend code (e.g., `.js`, `.ts`, `.jsx`, `.tsx`, `.vue`, `.svelte`)
   - Integration/API surfaces (e.g., handlers, controllers, routes)
   - Config, infrastructure, or test-only changes
3. For each changed area, determine:
   - What behavior was added or modified
   - Which existing tests (if any) already cover this behavior
   - Where new or expanded tests are needed

### Phase 2: Test Plan Design

Draft a concrete test plan for this commit:

1. **Scenarios to cover:**
   - List specific behaviors that need tests
   - Identify edge cases and error conditions

2. **Test layers to use:**
   - Unit tests for individual functions/methods
   - Integration tests for cross-component behavior
   - E2E tests for user-visible flows (if applicable)

3. **Test dependencies:**
   - Required fixtures, mocks, or test data
   - Any setup/teardown requirements

4. **Prioritization criteria:**
   - Safety-critical paths
   - Public/externally visible behavior
   - Complex logic and branching
   - Previously under-tested areas

### Phase 3: Test Implementation

Implement the tests specified in your plan:

1. **Follow existing conventions:**
   - Use existing test directories and naming patterns
   - Reuse shared test utilities and helpers
   - Match the style of existing tests in the repository

2. **Test quality standards:**
   - Each test should be focused on a single behavior
   - Tests must be deterministic (no flaky tests)
   - Tests should be readable and self-documenting
   - Include clear assertion messages

### Phase 4: Execution and Refinement

1. **Incremental testing:**
   - Run only the relevant tests while developing
   - Use focused test commands (specific packages, files, or test names)

2. **Validation:**
   - Once confident, run a broader test subset to check for regressions
   - Ensure all new tests pass consistently

3. **Failure diagnosis:**
   - If tests fail, prefer fixing implementation bugs exposed by the tests
   - Only adjust tests when they don't match the correct intended behavior

### Phase 5: Summary

Produce a concise summary including:

- Which files changed in the commit
- What tests were added or modified (by file and purpose)
- What behaviors are now covered that were not before
- The exact commands to run the relevant test suites

## Constraints

- **Do not remove or disable existing tests** unless clearly invalid; explain any such changes
- **Do not introduce new frameworks** or major structural changes; work within the existing test stack
- **Keep changes tightly scoped** to covering the latest commit's behavior, not the entire repository

## Examples

### Example: New HTTP Handler in Go

**Commit changes:** Added `internal/api/users.go` with a `CreateUser` handler

**Phase 1 output:**
```
Changed files:
- internal/api/users.go (new file)
  - Added CreateUser handler
  - Added userRequest/userResponse types
  - Added input validation logic

Existing test coverage: None (new file)
```

**Phase 2 output:**
```
Test Plan:
1. Unit tests for input validation
   - Valid request succeeds
   - Missing required fields return 400
   - Invalid email format returns 400
2. Integration tests for CreateUser handler
   - Successful user creation returns 201
   - Duplicate email returns 409
   - Database error returns 500
3. Mocks needed: UserRepository interface
```

**Phase 3 output:**
```
Created: internal/api/users_test.go
- TestCreateUser_Success
- TestCreateUser_MissingFields
- TestCreateUser_InvalidEmail
- TestCreateUser_DuplicateEmail
- TestCreateUser_DatabaseError
```

**Phase 5 summary:**
```
Files changed in commit: internal/api/users.go

Tests added:
- internal/api/users_test.go (5 tests covering CreateUser handler)

New coverage:
- Input validation for user creation requests
- Success and error paths for CreateUser handler
- Database error handling

Run tests: go test ./internal/api/... -v
```

---

Begin by performing the diff-based analysis for HEAD and drafting the test plan before writing or modifying any tests.

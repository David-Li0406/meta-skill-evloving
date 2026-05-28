---
name: e2e-testing
description: Orchestrate complete E2E test creation workflow from feature analysis to test implementation and healing. Use when a feature is developed and needs comprehensive E2E tests.
---

# E2E Test Workflow Skill

Orchestrates the complete E2E test creation workflow from feature analysis to test implementation
and healing.

## Purpose

USE this skill when:

- A feature has been developed and manually verified
- You need to create comprehensive E2E tests for new functionality
- You want to follow a structured approach to test creation

## Workflow Steps

### Step 1: Feature Analysis

**Goal**: Understand what was implemented and what needs testing.

**Actions**:

1. Check git staged changes: `git diff --cached --name-only`
2. Analyze staged files to understand the feature scope
3. Check `requirements/` directory for latest specifications:
   - Look for recent `.md` files
   - Find specifications matching the feature
4. If unclear, ASK USER:
   - Which feature should be tested?
   - Are there specific user flows to focus on?
   - Any edge cases to consider?

**Output**: Clear understanding of feature scope and test requirements.

---

### Step 2: Test Planning

**Goal**: Create comprehensive test plan using playwright-test-planner agent.

**Actions**:

1. INVOKE playwright-test-planner agent with context:
   - Feature description from analysis
   - User-specified focus areas (if provided)
   - Files that were changed
   - Requirements specifications
2. AGENT WILL:
   - Navigate to the feature in browser
   - Identify all interactive elements
   - Create detailed test scenarios
   - Document expected behaviors
3. WAIT for agent to complete and return test plan

**Output**: Detailed test plan with scenarios, steps, and assertions.

---

### Step 3: Test Implementation

**Goal**: Generate E2E tests using playwright-test-generator agent.

**Actions**:

1. INVOKE playwright-test-generator agent with:
   - Test plan from Step 2
   - Feature context
   - Component structure
2. AGENT WILL:
   - Create test files following project conventions
   - Use proper data-testid selectors
   - Implement fixtures where needed
   - Follow ESM module patterns
3. WAIT for agent to complete test generation

**Output**: Implemented test files ready to run.

---

### Step 4: Test Execution

**Goal**: Run tests and analyze results.

**Actions**:

1. RUN tests: `pnpm exec playwright test`
2. WAIT for execution to complete
3. ANALYZE results:
   - Check test output in terminal
   - Review `playwright-report/` directory
   - Identify passing and failing tests
4. CATEGORIZE failures:
   - App code issues (business logic, API, data)
   - Test code issues (selectors, assertions, timing)

**Output**: Test execution report with failure categorization.

---

### Step 5: Healing Loop

**Goal**: Fix failures until all tests pass.

**Actions**:

#### If App Code is Broken:

1. ANALYZE application code issues
2. CREATE fix plan:
   - Identify root cause
   - Plan necessary changes
   - Consider side effects
3. IMPLEMENT fixes:
   - Update application code
   - Verify fixes manually if needed
4. RE-RUN tests: `pnpm exec playwright test`
5. IF STILL FAILING: Return to beginning of Step 5

#### If Test Code is Broken:

1. INVOKE playwright-test-healer agent with:
   - Failing test file paths
   - Failure messages and stack traces
   - Playwright report details
2. AGENT WILL:
   - Debug failing tests
   - Fix selector issues
   - Adjust timing and waits
   - Update assertions
3. WAIT for agent to complete healing
4. RE-RUN tests: `pnpm exec playwright test`
5. IF STILL FAILING: Repeat test healing (max 3 iterations)
6. IF STILL FAILING after 3 iterations: ASK USER for guidance

**Output**: All tests passing or user intervention required.

---

## Success Criteria

- [ ] Feature scope clearly identified
- [ ] Comprehensive test plan created
- [ ] Tests implemented following project patterns
- [ ] All tests passing consistently
- [ ] Test report generated and reviewed

## Failure Recovery

**If stuck in healing loop:**

1. ANALYZE pattern of failures
2. CHECK if fundamental issue with test approach
3. ASK USER if:
   - Feature behavior is as expected
   - Test scenarios are still valid
   - Different testing approach needed

**If agent fails:**

1. DOCUMENT agent failure details
2. TRY manual intervention if possible
3. ASK USER for guidance if blocked

## Project-Specific Guidelines

**Test Selector Requirements:**

- VERIFY all components have data-testid attributes
- FOLLOW naming convention: `{feature}-{element}-{type}`
- REFERENCE .agents/test-ready-component-checklist.md

**Fixture Integration:**

- USE existing fixtures from `tests/fixtures/`
- IMPORT test and expect from `tests/fixtures/index.ts`
- FOLLOW .agents/e2e-testing-patterns.md

**Module Syntax:**

- USE ESM import statements exclusively
- ADD `with { type: "json" }` for JSON imports
- NEVER use `require()` in test files

## Example Usage

```
User: "I just implemented the meeting schedule feature. Can you create E2E tests for it?"
```

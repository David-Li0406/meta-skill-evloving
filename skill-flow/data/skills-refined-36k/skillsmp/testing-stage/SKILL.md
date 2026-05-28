---
name: testing-stage
description: Validate implementation through systematic testing after implement stage completes. Determines test type (unit/integration/e2e) based on task nature, runs pytest, and reports results. Stage 4 of dev-workflow pipeline. Use when user says "运行测试", "run tests", "test", or after implementation.
metadata:
  category: testing
  triggers: "run tests, test, validate, 运行测试"
allowed-tools: Read Bash(pytest:*) Bash(python:*)
---

# Testing Stage Skill

You are the **Quality Assurance Engineer** for the Modular RAG MCP Server. After implementation is complete, you MUST validate the work through systematic testing before proceeding to the next phase.

> **Prerequisite**: This skill runs AFTER `implement` has completed.
> Spec files are located at: `.github/skills/spec-sync/specs/`

---

## Testing Strategy Decision Matrix

**CRITICAL**: Test type should be determined by the **nature of the current task**. Read the task's "测试方法" from `specs/06-schedule.md` to decide.

| Task Characteristics | Recommended Test Type | Rationale |
|---------------------|----------------------|----------|
| Single module, no external dependencies | **Unit Tests** | Fast, isolated, repeatable |
| Factory/Interface definition only | **Unit Tests** (with mocks/fakes) | Verify routing logic without real backend |
| Module needs real DB/filesystem | **Integration Tests** | Need to verify interaction with real dependencies |
| Pipeline/workflow orchestration | **Integration Tests** | Need to verify multi-module coordination |
| CLI scripts or end-user entry points | **E2E Tests** | Verify complete user workflow |
| Cross-module data flow (Ingestion→Retrieval) | **Integration/E2E** | Verify data flows correctly between modules |

---

## Testing Objectives

1. **Verify Implementation Completeness**: Ensure all requirements from the spec have been implemented.
2. **Run Unit Tests**: Execute relevant pytest unit tests for the implemented module.
3. **Validate Integration Points**: Check that the new code integrates correctly with existing modules.
4. **Report Issues**: Provide actionable feedback if tests fail.

---

## Step 1: Identify Test Scope & Test Type

**Goal**: Determine what needs to be tested and **which type of tests** to run based on the current task phase.

### 1.1 Identify Modified Files
1. Read the task completion summary from Stage 3 (Implementation).
2. Identify which modules/files were created or modified.
3. Map files to their corresponding test files:
   - `src/libs/xxx/yyy.py` → `tests/unit/test_yyy.py`
   - `src/core/xxx/yyy.py` → `tests/unit/test_yyy.py`
   - `src/ingestion/xxx.py` → `tests/unit/test_xxx.py` or `tests/integration/test_xxx.py`

### 1.2 Determine Test Type (Smart Selection)

**CRITICAL**: The test type should be determined by the **nature of the current task**, not a fixed rule.

**Decision Logic**:

1. Read the task spec in `specs/06-schedule.md` to find the "测试方法" field
2. Apply the **Testing Strategy Decision Matrix** (see top of document)
3. Check task-specific test method in schedule:
   - `pytest -q tests/unit/test_xxx.py` → Run unit tests
   - `pytest -q tests/integration/test_xxx.py` → Run integration tests
   - `pytest -q tests/e2e/test_xxx.py` → Run E2E tests

**Output**:
```
────────────────────────────────────
 TEST SCOPE IDENTIFIED
────────────────────────────────────
Task: [C14] Pipeline 编排（MVP 串起来）
Modified Files:
- src/ingestion/pipeline.py

Test Type Decision:
- Task Nature: Pipeline orchestration (multi-module coordination)
- Spec Test Method: pytest -q tests/integration/test_ingestion_pipeline.py
- Selected: **Integration Tests** 

Rationale: This task wires multiple modules together,
requiring real interactions between loader, splitter,
transform, and storage components.
────────────────────────────────────
```

---

## Step 2: Execute Tests

**Goal**: Run the appropriate tests and capture results.

**Actions**:

### 2.1 Check if Tests Exist
```bash
# Check for existing test files
ls tests/unit/test_<module_name>.py
ls tests/integration/test_<module_name>.py
```

### 2.2 If Tests Exist - Run Them
```bash
# Run specific unit tests
pytest -v tests/unit/test_<module_name>.py

# Run with coverage if available
pytest -v --cov=src/<module_path> tests/unit/test_<module_name>.py
```

### 2.3 If Tests Don't Exist - Report Missing Tests
If the spec requires tests but none exist:

```
────────────────────────────────────────
 ⚠️ MISSING TESTS DETECTED
────────────────────────────────────────
Module: <module_name>
Expected Test File: tests/unit/test_<module_name>.py

Status: NOT FOUND

Action Required:
  Return to Stage 3 (implement) to create tests
  following the test patterns in existing test files.
────────────────────────────────────────
```

**Action**: Return `MISSING_TESTS` signal to workflow orchestrator to go back to implement stage.

---

## Step 3: Analyze Results

**Goal**: Interpret test results and determine next action.

### 3.1 Test Passed 
If all tests pass:
```
────────────────────────────────────────
 TESTS PASSED
────────────────────────────────────────
Module: <module_name>
Tests Run: X
Tests Passed: X
Coverage: XX% (if available)

Ready to proceed to next phase.
────────────────────────────────────────
```
**Action**: Return `PASS` signal to workflow orchestrator.

### 3.2 Test Failed 
If any tests fail:
```
────────────────────────────────────────
 TESTS FAILED
────────────────────────────────────────
Module: <module_name>
Tests Run: X
Tests Failed: Y

Failed Tests:
1. test_xxx - AssertionError: expected A, got B
2. test_yyy - ImportError: module not found

Root Cause Analysis:
- [Analyze the failure and identify the issue]

Suggested Fix:
- [Provide specific fix suggestions]
────────────────────────────────────────
```
**Action**: Return `FAIL` signal with detailed feedback to `implement` for iteration.

---

## Step 4: Feedback Loop

**Goal**: Enable iterative improvement until tests pass.

### If Tests Failed:
1. **Generate Fix Report**: Create a structured report with:
   - Failed test name
   - Error message
   - Stack trace summary
   - File and line number of failure
   - Suggested fix approach

2. **Return to Implementation**: Pass the fix report back to Stage 3 (implement) for correction.

3. **Re-test**: After implementation updates, run tests again.

### Iteration Limit:
- **Maximum 3 iterations** per task to prevent infinite loops.
- If still failing after 3 iterations, escalate to user for manual intervention.

---

## Testing Standards

### Test Naming Convention
- `test_<function>_<scenario>_<expected_result>`
- Example: `test_embed_empty_input_returns_empty_list`

### Test Categories (pytest markers)
```python
@pytest.mark.unit       # Fast, isolated tests
@pytest.mark.integration  # Tests with real dependencies
@pytest.mark.e2e        # End-to-end tests
@pytest.mark.slow       # Long-running tests
```

### Mock Strategy
- **Unit Tests**: Mock all external dependencies (LLM, DB, HTTP)
- **Integration Tests**: Use real local dependencies, mock external APIs
- **E2E Tests**: Minimal mocking, test actual behavior

---

## Validation Checklist

Before marking tests as complete, verify:

- [ ] All new public methods have at least one test
- [ ] Tests follow the naming convention
- [ ] Tests are placed in the correct directory (unit/integration/e2e)
- [ ] Tests use appropriate mocking (no real API calls in unit tests)
- [ ] Test assertions match spec requirements
- [ ] No hardcoded paths or credentials in tests
- [ ] Tests can run in isolation (no order dependency)

---

## Important Rules

1. **No Skipping Tests**: If spec says "tests needed", tests must exist.
2. **Fast Feedback**: Unit tests should complete in < 10 seconds.
3. **Deterministic**: Tests must not have random failures.
4. **Independence**: Each test must be able to run independently.
5. **Clear Failures**: Failed tests must provide actionable error messages.

---

---
name: qe-iterative-loop
description: Use this skill when you need to implement autonomous quality engineering iteration loops to ensure tests pass, coverage targets are met, and quality gates are satisfied.
---

# Skill body

## Overview

The QE Iterative Loop is a specialized approach for **Quality Engineering workflows** that enables autonomous, self-correcting quality cycles. AI agents iterate until quality objectives are achieved, such as passing tests, meeting coverage targets, satisfying quality gates, or stabilizing flaky tests.

## Why QE Benefits from Iteration

Quality Engineering has **objective, measurable success criteria**:
- Tests either pass or fail (exit code 0 vs non-zero)
- Coverage is quantifiable (e.g., 78.5% vs 80% target)
- Quality gates have binary outcomes (pass/fail)
- Contract validation has clear schemas

This makes QE ideal for iterative loops, as we can clearly define when the process is complete.

## Prerequisites

- AQE v3 fleet initialized
- Test framework configured (e.g., Jest, Vitest, Pytest)
- Coverage tooling (e.g., c8, istanbul, coverage.py)
- Quality gate definitions

## Quick Start

### Pattern 1: Test Fix Iteration

```bash
# Task: Fix all failing tests
/qe-loop "Run npm test and fix all failing tests.
Success: npm test exits with code 0
Output <promise>TESTS_GREEN</promise> when all tests pass."
```

### Pattern 2: Coverage Target Iteration

```bash
# Task: Achieve 80% coverage
/qe-loop "Increase test coverage to 80%.
Success: Coverage report shows >= 80%
Output <promise>COVERAGE_MET</promise> when target achieved."
```

### Pattern 3: Quality Gate Iteration

```bash
# Task: Pass all quality gates
/qe-loop "Pass all quality gates for deployment.
Gates:
- Unit tests: pass
- Integration tests: pass
- Coverage: >= 80%
- No critical vulnerabilities
- Performance < 200ms P95
Output <promise>QUALITY_GATES_PASSED</promise> when all pass."
```

## QE Iteration Patterns

### Pattern 1: Test-Fix Iteration Loop

**Goal**: Ensure all tests pass

```markdown
## QE Test-Fix Loop

### Success Criteria
- `npm test` (or equivalent test command) returns exit code 0
- No skipped tests (unless explicitly allowed)
- No pending tests

### Iteration Steps
1. Run the full test suite.
2. Parse output for failures.
3. Analyze the first failure:
   - Identify the failing test file.
   - Understand the assertion that failed.
```
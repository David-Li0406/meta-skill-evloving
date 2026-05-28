---
name: mutation-testing
description: Use this skill when analyzing branch code to verify test effectiveness and identify weak or missing tests.
---

# Mutation Testing

Mutation testing answers the question: **"Are my tests actually catching bugs?"** Code coverage tells you what code your tests execute, while mutation testing reveals if your tests would **detect changes** to that code. A test suite with 100% coverage can still miss significant bugs.

## Core Concept

**The Mutation Testing Process:**

1. **Generate mutants**: Introduce small bugs (mutations) into production code.
2. **Run tests**: Execute your test suite against each mutant.
3. **Evaluate results**: If tests fail, the mutant is "killed" (good). If tests pass, the mutant "survived" (bad - your tests missed the bug).

**The Insight**: A surviving mutant represents a bug your tests wouldn't catch.

## When to Use This Skill

Use mutation testing analysis when:

- Reviewing code changes on a branch.
- Verifying test effectiveness after Test-Driven Development (TDD).
- Identifying weak tests that appear to have coverage.
- Finding missing edge case tests.
- Validating that refactoring didn't weaken the test suite.

**Integration with TDD:**

```
TDD Workflow                    Mutation Testing Validation
┌─────────────────┐             ┌─────────────────────────────┐
│ RED: Write test │             │                             │
│ GREEN: Pass it  │──────────►  │ After GREEN: Verify tests   │
│ REFACTOR        │             │ would kill relevant mutants │
└─────────────────┘             └─────────────────────────────┘
```

## Systematic Branch Analysis Process

When analyzing code on a branch, follow this systematic process:

### Step 1: Identify Changed Code

```bash
# Get files changed on the branch
git diff main...HEAD --name-only | grep -E '\.(ts|js|tsx|jsx)$' | grep -v '\.test\.'

# Get detailed diff for analysis
git diff main...HEAD -- src/
```

### Step 2: Generate Mental Mutants

For each changed function/method, mentally apply mutation operators.

### Step 3: Verify Test Coverage

For each potential mutant, ask:

1. **Is there a test that exercises this code path?**
2. **Would that test FAIL if this mutation were applied?**
3. **Is the assertion specific enough to catch this change?**

### Step 4: Document Findings

Categorize findings:

| Category | Description | Action Required |
|----------|-------------|-----------------|
| Killed   | Test would fail against the mutant. | None |
| Survived | Test passed against the mutant. | Improve tests |
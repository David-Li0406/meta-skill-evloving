---
name: foundry-test
description: Systematic test debugging with 5-phase investigation workflow. Use when debugging test failures, investigating complex errors, or when AI consultation would help. Uses native test commands with optional AI consultation for complex failures.
---

# Test Runner Skill

## Overview

The **Skill(foundry:foundry-test)** skill provides systematic test debugging with a 5-phase investigation workflow. It guides debugging complex test failures and leverages AI consultation when available.

**When to use this skill:**
- Debugging test failures that aren't obvious
- Systematic investigation needed (flaky tests, complex failures)
- AI consultation would help diagnose the issue

**When NOT to use this skill:**
- Simple test runs (just use `pytest`, `go test`, `npm test` directly)
- Tests are passing
- Failure cause is obvious

## Core Workflow

> `[x?]`=decision · `(GATE)`=user approval · `→`=sequence · `↻`=loop

```
- **Entry** → Run failing test(s)
  - [pass?] → **Exit**: Done
  - [else] → Categorize failure → Form hypothesis → Gather context
    - [explore preferred?] → Explore subagent
    - [else] → Targeted lookup
    - [research available?] → `research action="chat"` → Consult (MANDATORY)
    - [else] → skip
    - Implement fix → Verify specific
      - [pass?] → Run full suite
        - [pass?] → **Exit**: Done
        - [else] → ↻ back to Form hypothesis
      - [else] → ↻ back to Form hypothesis
```

**Decision rules:**
- Tests pass? Done.
- Simple fix (typo/obvious)? Fix, then verify.
- Complex/unclear? Investigate, consult AI, fix, verify.

## Phase 1: Run Tests

Use native test commands:

```bash
# Python
pytest tests/test_module.py::test_function -vvs

# Go
go test -v -run TestName ./...

# JavaScript
jest path/to/test.js -t "test name"
npm test
```

## Phase 2: Investigate Failures

**Categorize the failure:**

| Category | Description |
|----------|-------------|
| Assertion | Expected vs actual mismatch |
| Exception | Runtime errors (language-specific) |
| Import | Missing dependencies or module issues |
| Setup | Fixture, configuration, or initialization issues |
| Timeout | Performance or hanging issues |
| Flaky | Non-deterministic failures |

**Extract key information:**
- Test file and function name
- Line number where failure occurred
- Error type and message
- Full stack trace

**Form hypothesis:** What's causing the failure?

> For detailed failure categories, see `references/failure-categories.md`

## Phase 3: Gather Code Context

Use **Explore subagents** (preferred) for code context, or `Glob`, `Grep`, and `Read` for targeted lookups.

**Subagent selection:**
- **Explore (quick)** - Find related test files
- **Explore (medium)** - Understand module dependencies
- **Explore (very thorough)** - Multi-file state/fixture investigation

> For detailed subagent patterns, see `references/subagent-patterns.md`

## Phase 4: AI Consultation

**Mandatory for complex failures when research tools are available.**

**Standard consultation (most cases):**
```
mcp__plugin_foundry_foundry-mcp__research action="chat" prompt="..." system_prompt="You are debugging a test failure."
```

**Multi-perspective analysis (flaky tests, architectural issues):**
```
mcp__plugin_foundry_foundry-mcp__research action="consensus" prompt="..." strategy="synthesize"
```

**When to use which:**
- `chat` - Standard debugging, quick diagnosis
- `consensus` - Complex failures, want multiple AI perspectives, flaky tests
- `thinkdeep` - Systematic hypothesis-driven investigation for complex issues

**CRITICAL:** Read [references/tool-selection.md](./references/tool-selection.md) before AI consultation. Contains required prompt templates and strategy parameters.

## Phase 5: Fix & Verify

1. Synthesize findings from investigation + AI recommendations
2. Implement fix using Edit tool
3. Verify with specific test (native command)
4. Run full suite to check for regressions

### Requirement Discovery (SDD Integration)

When debugging reveals missing spec requirements, document them:

```
mcp__plugin_foundry_foundry-mcp__task action="add-requirement" spec_id={spec-id} task_id={task-id} requirement="Handle empty input array gracefully"
```

**When to use:**
- Test failure reveals undocumented edge case
- Fix requires behavior not in acceptance criteria
- Investigation uncovers missing validation rule

## Runner-Specific Notes

### Python (pytest)
- **Run specific:** `pytest tests/test_file.py::test_name -vvs`
- **Debug mode:** `pytest --pdb tests/test_file.py::test_name`
- **Markers:** `-m "unit"`, `-m "not slow"`
- **Coverage:** `pytest --cov=src --cov-report=term-missing`

### Go
- **Run specific:** `go test -v -run TestName ./...`
- **Race detection:** `go test -race ./...`
- **Coverage:** `go test -cover -coverprofile=coverage.out ./...`
- **Debug:** `dlv test -- -test.run TestName`

### JavaScript (Jest)
- **Run specific:** `jest path/to/test.js -t "test name"`
- **Watch mode:** `jest --watch`
- **Debug:** `node --inspect-brk node_modules/.bin/jest --runInBand`
- **Coverage:** `jest --coverage`

### npm test
- **Standard:** `npm test`
- **Pass args:** `npm test -- --specific-flag`

## Detailed Reference

- Failure categories → `references/failure-categories.md`
- Investigation patterns → `references/investigation.md`
- Subagent patterns → `references/subagent-patterns.md`
- AI prompt templates → `references/tool-selection.md`
- Common fixes → `references/common-fixes.md`
- Troubleshooting → `references/troubleshooting.md`

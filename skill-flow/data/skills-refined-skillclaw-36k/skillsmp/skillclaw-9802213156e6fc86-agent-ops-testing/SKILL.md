---
name: agent-ops-testing
description: Use this skill when designing tests, running test suites, or analyzing test results beyond baseline checks.
---

# Testing Workflow

**Works with or without `aoc` CLI installed.** Issue tracking can be done via direct file editing.

## Purpose

Provide structured guidance for test design, execution, and analysis that goes beyond baseline capture. This skill covers test strategy during planning, incremental testing during implementation, and coverage analysis.

## Test Commands (from constitution)

```bash
# Python (uv/pytest)
uv run pytest                           # Run all tests
uv run pytest tests/ -v                 # Verbose output
uv run pytest tests/ -m "not slow"      # Skip slow tests
uv run pytest tests/ --tb=short -q      # Quick summary
uv run pytest --cov=src --cov-report=html  # Coverage report

# TypeScript/Node (vitest/jest)
npm run test                            # Run all tests
npm run test -- --coverage              # With coverage

# .NET (dotnet test)
dotnet test                             # Run all tests
dotnet test --collect:"XPlat Code Coverage"  # With coverage
```

## Issue Tracking (File-Based — Default)

| Operation | How to Do It |
|-----------|--------------|
| Create test issue | Append to `.agent/issues/medium.md` with type `TEST` |
| Create bug from failure | Append to `.agent/issues/high.md` with type `BUG` |
| Log test results | Edit issue's `### Log` section in priority file |

### Example: Post-Test Issue Creation (File-Based)

1. Increment `.agent/issues/.counter`
2. Append issue to appropriate priority file
3. Add log entry with test run results

## CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Operation | Command |
|-----------|---------|
| Create test issue | `aoc issues create --type TEST --title "Add tests for..."` |
| Create bug from failure | `aoc issues create --type BUG --priority high --title "Test failure: ..."` |
| Log test results | `aoc issues update <ID> --log "Tests: 45 pass, 2 fail"` |

## Test Isolation (MANDATORY)

**Tests must NEVER create, modify, or delete files in the project folder.**
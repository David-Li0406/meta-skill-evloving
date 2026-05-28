---
name: testing-guide
description: Use this skill when writing tests, discussing test coverage, test strategy, or test naming, following the testing pyramid standards.
---

# Skill Body

## Purpose

This skill provides testing pyramid standards and best practices for systematic testing, supporting both ISTQB and Industry Pyramid frameworks.

## Framework Selection

| Framework | Levels | Best For |
|-----------|--------|----------|
| **ISTQB** | UT → IT/SIT → ST → AT/UAT | Enterprise, compliance, formal QA |
| **Industry Pyramid** | UT (70%) → IT (20%) → E2E (10%) | Agile, DevOps, CI/CD |

**Note on Integration Testing abbreviation:**
- **IT** (Integration Testing): Agile/DevOps communities
- **SIT** (System Integration Testing): Enterprise/ISTQB contexts
- Both refer to the same testing level.

## Quick Reference

### Testing Pyramid (Industry Standard)

```
              ┌─────────┐
              │   E2E   │  ← 10% (Fewer, slower)
             ─┴─────────┴─
            ┌─────────────┐
            │   IT/SIT    │  ← 20% (Integration)
           ─┴─────────────┴─
          ┌─────────────────┐
          │       UT        │  ← 70% (Unit)
          └─────────────────┘
```

### Test Levels Overview

| Level | Scope | Speed | Dependencies |
|-------|-------|-------|-------------|
| **UT** | Single function/class | < 100ms | Mocked |
| **IT/SIT** | Component interaction | 1-10s | Real DB (containerized) |
| **ST** | Full system (ISTQB) | Minutes | Production-like |
| **E2E** | User journeys | 30s+ | Everything real |
| **AT/UAT** | Business validation (ISTQB) | Varies | Everything real |

### Coverage Targets

| Metric | Minimum | Recommended |
|--------|---------|-------------|
| Line | 70% | 85% |
| Branch | 60% | 80% |
| Function | 80% | 90% |

## Detailed Guidelines

For complete standards, see:
- [Testing Pyramid](./testing-pyramid.md)

### AI-Optimized Format (Token-Efficient)

For AI assistants, use the YAML format files for reduced token usage:
- Base standard: `ai/standards/testing.ai.yaml`
- Framework options:
  - ISTQB Framework: `ai/options/testing/istqb-framework.ai.yaml`
  - Industry Pyramid: `ai/options/testing/industry-pyramid.ai.yaml`
- Test level options:
  - Unit Testing: `ai/options/testing/unit-testing.ai.yaml`
  - Integration Testing: `ai/options/testing/integration-testing.ai.yaml`
  - System Testing: `ai/options/testing/system-testing.ai.yaml`
  - E2E Testing: `ai/options/testing/e2e-testing.ai.yaml`

## Naming Conventions

### File Naming

```
[ClassName]Tests.cs       # C#
[ClassName].test.ts       # TypeScript
[class_name]_test.py      # Python
[class_name]_test.go      # Go
```

### Method Naming

```
[MethodName]_[Scenario]_[ExpectedResult]()
should_[behavior]_when_[condition]()
```
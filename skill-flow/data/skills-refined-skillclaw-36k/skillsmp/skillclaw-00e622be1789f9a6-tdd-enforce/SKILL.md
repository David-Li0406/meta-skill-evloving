---
name: tdd-enforce
description: Use this skill when you want to configure Test-Driven Development (TDD) enforcement through pre-commit hooks and CI coverage gates to ensure code quality and adherence to TDD practices.
---

# TDD Enforce Skill

## Purpose

Configure Test-Driven Development enforcement through pre-commit hooks, CI coverage gates, and automated test execution. This ensures that code cannot be committed or merged without adequate test coverage.

## Research Foundation

| Principle | Source | Reference |
|-----------|--------|-----------|
| TDD Methodology | Kent Beck (2002) | "Test-Driven Development by Example" |
| 80% Coverage | Google Testing Blog (2010) | [Code Coverage Goal](https://testing.googleblog.com/2010/07/code-coverage-goal-80-and-no-less.html) |
| Pre-commit Hooks | Industry Best Practice | [Husky](https://typicode.github.io/husky/), [pre-commit](https://pre-commit.com/) |
| CI Gates | ISTQB CT-TAS | [Test Automation Strategy](https://istqb.org/certifications/certified-tester-test-automation-strategy-ct-tas/) |

## When This Skill Applies

- User asks to "set up TDD" or "enforce test-first"
- User wants to "add coverage gates" or "block commits without tests"
- User mentions "pre-commit hooks for tests" or "CI test gates"
- Project needs test quality enforcement
- Brownfield project needs TDD adoption

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Set up TDD enforcement" | Configure pre-commit + CI gates |
| "Add coverage gates" | Configure CI coverage thresholds |
| "Block commits without tests" | Set up pre-commit test hooks |
| "Enforce test-first development" | Full TDD setup |
| "Run tests on commit" | Configure pre-commit test execution |
| "Check if tests exist for new code" | Configure test presence validation |

## Configuration Options

### Coverage Thresholds

```yaml
coverage:
  line: 80        # Google standard: 80% minimum
  branch: 75      # Branch coverage threshold
  function: 90    # Function coverage threshold
  critical_paths: 100  # Auth, payments, validation
```

### Enforcement Levels

| Level | Pre-commit | CI Gate | Description |
|-------|-----------|---------|-------------|
| `strict` | Block | Fail | No exceptions, 100% enforcement |
| `standard` | Warn + Block | Fail | Standard TDD enforcement |
| `gradual` | Warn | Warn | For TDD adoption in brownfield |
| `audit` | Log only | Report | Visibility without blocking |

## Implementation Process

### 1. Detect Project Type

```python
def detect_project_type():
    # Implementation to detect project type
    pass
```
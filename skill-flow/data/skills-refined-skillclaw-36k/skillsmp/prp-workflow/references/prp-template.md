# PRP Template

Use this template when generating PRPs. Adapt sections as needed for the specific feature.

```yaml
name: "[Feature Name] PRP"
description: |

## Purpose
[What this PRP enables the AI to build]

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Follow all rules in CLAUDE.md (if exists)

---

## Goal
[What needs to be built - be specific about the end state]

## Why
- [Business value and user impact]
- [Integration with existing features]
- [Problems this solves and for whom]

## What
[User-visible behavior and technical requirements]

### Success Criteria
- [ ] [Specific measurable outcome 1]
- [ ] [Specific measurable outcome 2]
- [ ] [Specific measurable outcome 3]

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: [Official API docs URL]
  why: [Specific sections/methods you'll need]

- file: [path/to/example.py]
  why: [Pattern to follow, gotchas to avoid]

- doc: [Library documentation URL]
  section: [Specific section]
  critical: [Key insight that prevents common errors]
```

### Current Codebase Tree
```bash
[Output from tree command - shows current structure]
```

### Desired Codebase Tree
```bash
[New files to be added with their responsibilities]
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: [Library name] requires [specific setup]
# CRITICAL: [Framework] version [X] has [specific behavior]
# CRITICAL: [Common pitfall to avoid]
```

## Implementation Blueprint

### Data Models and Structure
[Define core data structures, Pydantic models, ORM models, etc.]

### List of Tasks
```yaml
Task 1: [Task Name]
  MODIFY/CREATE [file path]:
    - [Specific action 1]
    - [Specific action 2]
  PATTERN: [Reference to similar code]

Task 2: [Task Name]
  ...
```

### Per Task Pseudocode
```python
# Task 1: [Task Name]
def feature_function(param: Type) -> Result:
    # PATTERN: Always validate input (see file:line)
    # GOTCHA: This library requires X
    # CRITICAL: API has rate limit of Y
    pass
```

### Integration Points
```yaml
DATABASE:
  - migration: [SQL or migration description]
  - index: [Index requirements]

CONFIG:
  - add to: [config file path]
  - pattern: [How to add config]

ROUTES/ENDPOINTS:
  - add to: [router file]
  - pattern: [How to register]
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Language-specific linting commands
# Python: ruff check . --fix && mypy .
# TypeScript: eslint . --fix && tsc --noEmit
# Go: go fmt ./... && go vet ./...
```

### Level 2: Unit Tests
```python
# Define required test cases:
# 1. Happy path test
# 2. Edge case test
# 3. Error handling test
```

```bash
# Run command: pytest tests/ -v
```

### Level 3: Integration Test
```bash
# Manual test commands (curl, CLI, etc.)
```

## Final Validation Checklist
- [ ] All tests pass
- [ ] No linting errors
- [ ] No type errors
- [ ] Manual test successful
- [ ] Error cases handled
- [ ] Documentation updated

---

## Anti-Patterns to Avoid
- Don't create new patterns when existing ones work
- Don't skip validation steps
- Don't ignore failing tests
- Don't hardcode values that should be config
- [Domain-specific anti-patterns]
```

## PRP Quality Checklist

Before finalizing, verify:
- [ ] All necessary context included
- [ ] Validation gates are executable
- [ ] References existing patterns with file paths
- [ ] Clear implementation path with specific tasks
- [ ] Error handling documented
- [ ] Success criteria are measurable

Score the PRP confidence level (1-10) for one-pass implementation success.

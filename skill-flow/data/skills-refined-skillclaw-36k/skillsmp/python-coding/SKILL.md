---
name: python-coding
description: Comprehensive Python development guidance covering best practices, coding patterns, testing strategies, and code quality standards.
version: 1.0.0
author: AIECS Team
tags:
  - python
  - development
  - coding
  - testing
  - best-practices
dependencies: []
recommended_tools:
  - python
  - pytest
  - ruff
  - mypy
scripts:
  validate-python:
    path: scripts/validate-python.sh
    mode: subprocess
    description: Validates Python syntax and runs basic linting checks
    parameters:
      file_path:
        type: string
        required: true
        description: Path to the Python file to validate
  run-tests:
    path: scripts/run-tests.sh
    mode: subprocess
    description: Runs pytest on a specified test file or directory
    parameters:
      test_path:
        type: string
        required: false
        description: Path to test file or directory (defaults to current directory)
      verbose:
        type: boolean
        required: false
        description: Run tests with verbose output
---

# Python Coding Skill

This skill provides comprehensive guidance for Python development, including best practices, coding patterns, testing strategies, and code quality standards.

## When to Use This Skill

Activate this skill when:
- Writing new Python code or modules
- Refactoring existing Python code
- Setting up Python project structure
- Writing or improving unit tests
- Debugging Python applications
- Reviewing code for best practices

## Key Principles

### PEP 8 Compliance
Follow Python's official style guide for consistent, readable code:
- Use 4 spaces for indentation
- Limit lines to 88 characters (Black formatter default)
- Use snake_case for functions and variables
- Use PascalCase for class names
- Add blank lines to separate logical sections

### Type Hints
Use type annotations for better code clarity and IDE support:
```python
def process_data(items: list[str], limit: int = 10) -> dict[str, int]:
    ...
```

### Testing Practices
- Write tests alongside code using pytest
- Aim for high test coverage on critical paths
- Use fixtures for reusable test setup
- Mock external dependencies appropriately

## Quick Reference

### Common Patterns

| Pattern | Use Case |
|---------|----------|
| Context Manager | Resource management (files, connections) |
| Dataclass | Simple data containers |
| Protocol | Structural subtyping / duck typing |
| Generator | Memory-efficient iteration |

### Essential Commands

```bash
# Validate Python syntax
python -m py_compile your_file.py

# Run tests
pytest test_file.py -v

# Type checking
mypy your_module/

# Linting
ruff check your_module/
```

## Resources

See `references/best-practices.md` for detailed guidelines and `examples/code-patterns.py` for code samples.


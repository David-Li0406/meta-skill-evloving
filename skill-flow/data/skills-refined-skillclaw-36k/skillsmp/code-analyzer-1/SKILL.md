---
name: code-analyzer
description: Perform static analysis on cvp/ modules for code quality reports. Use for code review or quality checks.
allowed-tools: Read, Glob, Grep, Bash
---

# Code Analyzer

Run static analysis and generate quality reports for cvp/ modules.

## Analysis

1. **Complexity**: Cyclomatic complexity (warn if >10), function length (warn if >50 lines)
2. **Type hints**: Missing annotations, excessive `Any` usage
3. **Quality**: Unused imports/variables, duplicate patterns
4. **Dependencies**: Circular dependencies, external libraries

## Commands

```bash
./flake8.sh {path}
./mypy.sh {path}
```

## Report Format

Output as markdown table:
- File/class/function counts
- Average complexity
- Type hint coverage
- Issues with suggested fixes

Per CLAUDE.md: Fix root causes, don't use `# type: ignore` or `# noqa`.

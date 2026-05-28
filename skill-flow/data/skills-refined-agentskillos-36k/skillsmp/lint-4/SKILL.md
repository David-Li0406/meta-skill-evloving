---
name: lint
description: Run code linting and static analysis. Use to check code quality, find issues, or auto-fix style problems.
allowed-tools: Bash, Read, Edit, Glob
---

# Lint - argus

Run code linting and static analysis.

## Command

```bash
make lint
```

## Description

Run linter

## On Failure

- Review each linting error
- Auto-fix when possible using `--fix` flag
- For remaining issues, fix manually
- Don't ignore warnings without good reason

## Success Criteria

- No linting errors
- Warnings are reviewed and addressed

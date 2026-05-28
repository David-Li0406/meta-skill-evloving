---
name: static-analysis-and-linting
description: Use this skill to perform static analysis and linting on a codebase to ensure code quality and correctness.
---

# Static Analysis and Linting

Run static analysis (linting and type checking) to verify code correctness and quality.

## Steps

1. Read the README, Makefile, or package.json to find the lint/check commands.
2. Execute the linting command, typically using `make lint`. If a separate type checking command exists, run both.
3. Review each linting error. Auto-fix when possible using the `--fix` flag, and manually address any remaining issues.
4. Fix any errors found before proceeding, ensuring no linting errors remain and all warnings are reviewed and addressed.

## Success Criteria

- No linting errors.
- All warnings are reviewed and addressed.
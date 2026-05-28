---
name: static-analysis-and-linting
description: Use this skill to run static analysis and linting on a codebase to ensure code quality and correctness.
---

# Static Analysis and Linting

Run linting and type checking to verify code correctness and quality.

## Steps

1. Read the README, Makefile, or package.json to find the lint/check commands.
2. Run the linting command (e.g., `make lint`). If a separate type checking command exists, run both.
3. Review each linting error and auto-fix when possible using the `--fix` flag. For remaining issues, fix them manually.
4. Ensure no linting errors remain and that all warnings are reviewed and addressed.
5. Fix any errors found before proceeding.

## Success Criteria

- No linting errors.
- All warnings are reviewed and addressed.
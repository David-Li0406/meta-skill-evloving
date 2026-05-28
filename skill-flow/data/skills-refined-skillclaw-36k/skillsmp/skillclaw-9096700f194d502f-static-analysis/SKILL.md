---
name: static-analysis
description: Use this skill when you need to run static analysis and linting on your codebase to ensure code quality and correctness.
---

# Static Analysis and Linting

Run static analysis and linting to verify code correctness and quality.

## Steps

1. Read the README, Makefile, or package.json to find the lint/check commands.
2. Run the linting command (e.g., `make lint`). If a separate type checking command exists, run both.
3. Review each linting error. Auto-fix when possible using the `--fix` flag.
4. For remaining issues, fix them manually. Don't ignore warnings without good reason.
5. Ensure there are no linting errors and that all warnings are reviewed and addressed before proceeding.
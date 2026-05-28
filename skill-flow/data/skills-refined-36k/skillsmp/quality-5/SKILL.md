---
name: quality
description: Ensure code quality and correctness. Run tests, validation, and linters.
---

# Quality Skill

Use this skill to verify your work before requesting reviews.
The `verify` command is the standard "Definition of Done" check for this project.

## Commands

### Verify (Run All Checks)
Runs both unit tests and task validation.
**Run this before every commit/review.**
Command: `python3 scripts/quality.py verify`

### Run Tests
Run the project's test suite or specific tests.
Command: `python3 scripts/quality.py test [pattern] [-v] [--format json]`
Examples:
- `python3 scripts/quality.py test` (All tests)
- `python3 scripts/quality.py test tests/test_memory.py` (Specific file)
- `python3 scripts/quality.py test scripts.lib.utils` (Specific module)

### Run Linters
Run available linters (flake8, pylint) on the codebase or specific files.
Command: `python3 scripts/quality.py lint [files...]`

### Map (Scaffold Test)
Create a new test file corresponding to a source file.
Command: `python3 scripts/quality.py map <src_file>`
Example: `python3 scripts/quality.py map scripts/my_script.py` -> creates `tests/scripts/test_my_script.py`

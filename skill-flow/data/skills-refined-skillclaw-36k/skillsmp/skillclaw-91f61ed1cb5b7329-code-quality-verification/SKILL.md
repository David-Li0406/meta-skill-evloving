---
name: code-quality-verification
description: Use this skill when you need to verify code changes for quality, correctness, and adherence to best practices after modifications.
---

# Code Quality Verification Skill

This skill helps in verifying the quality of code changes by checking for correctness, style issues, and potential bugs.

## Features

- Check for file changes
- Review code correctness
- Run tests (if available)
- Verify build success
- Perform lint checks
- Identify potential issues

## Verification Steps

1. **File Change Verification**
   - Confirm that expected files have been modified.
   - Ensure there are no unintended file changes.

2. **Code Quality Checks**
   - Ensure there are no lint errors.
   - Check for type errors.

3. **Functionality Verification**
   - Ensure all tests pass.
   - Confirm that the build is successful.

## Output

- `status`: success | warning | failure
- `changes`: list of modified files
- `test_results`: results of the tests (if applicable)
- `issues`: identified problems

## Usage Scenarios

- After making code changes, use this skill to ensure quality before merging.
- During code reviews to provide feedback on potential issues.
- When analyzing code for refactoring or debugging purposes.
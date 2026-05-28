---
name: code-review
description: Use this skill when you need to analyze the differences between your current branch and the base branch before merging, ensuring code quality and adherence to best practices.
---

# Code Review Skill

This skill provides a comprehensive framework for conducting code reviews, focusing on quality assurance and best practices.

## Purpose of Code Review

- **Early Bug Detection**: Identify issues before they reach the reviewer.
- **Quality Improvement**: Enhance readability, maintainability, and performance of the code.
- **Reviewer Support**: Reduce the reviewer's workload by providing clear and high-quality changes.
- **Documentation Quality**: Improve the quality of explanations in pull requests (PRs).

## When to Use

- Before creating a pull request (PR).
- After completing a feature.
- When requested to review changes.

## Review Steps

1. **Fetch Differences**: Compare your current branch with the base branch (usually `main`).
   ```bash
   git diff main...HEAD
   ```

2. **Analyze Changes**: Review the list of changed files and their statistics.
   ```bash
   git diff main...HEAD --name-only
   git diff main...HEAD --stat
   ```

3. **Review Criteria**: Check your code against the following criteria:

| Aspect               | Checkpoints                                         |
| -------------------- | --------------------------------------------------- |
| **Intended Changes** | Ensure no unintended changes are included.          |
| **Code Quality**     | Assess readability, maintainability, and naming conventions. |
| **Debug Code Removal** | Confirm removal of debug statements (e.g., `console.log`). |
| **Error Handling**   | Verify proper error handling is implemented.        |
| **Test Coverage**    | Ensure tests are added for the changes made.       |
| **Documentation**    | Check if necessary documentation is updated.       |
| **Security**         | Look for potential vulnerabilities.                 |
| **Performance**      | Identify any inefficient implementations.           |
| **Commit Granularity** | Ensure commits are focused on single purposes.    |

4. **Review Commits**: Examine each commit for:
   - Appropriate commit messages.
   - Logical flow between commits.
   - Independent review and revert capability.

   ```bash
   git log main...HEAD --oneline
   git show <commit-hash>
   ```

5. **AI-Assisted Review**: Optionally, use an AI agent to assist in reviewing the differences.
   ```bash
   "Please review the differences from the main branch."
   ```

## Checklist for Code Review

### Change Verification

- [ ] Only intended changes are included.
- [ ] Debug code has been removed.
- [ ] Code quality is appropriate.

### Quality Assurance

- [ ] Error handling is adequate.
- [ ] Tests have been added.
- [ ] Documentation is updated.
- [ ] No security issues are present.
- [ ] Performance issues are addressed.

### Commit Review

- [ ] Commit messages are appropriate.
- [ ] Commit granularity is correct (one feature per commit).
- [ ] Each commit is independently reviewable and testable.

## Example Usage

### Example 1: Pre-PR Code Review

```bash
# 1. Check differences
git diff main...HEAD --stat

# 2. Review file list for unintended changes
git diff main...HEAD --name-only

# 3. Review detailed differences
git diff main...HEAD

# 4. Optionally, use AI for review
"Please review the differences from the main branch."

# 5. Fix any issues and commit again
```

### Example 2: Pre-Commit Code Review

```bash
# 1. Check differences before committing
git diff
```
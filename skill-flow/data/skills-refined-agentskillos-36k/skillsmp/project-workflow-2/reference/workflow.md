# Workflow Guidelines

> **Version**: 2.0.0
> **Last Updated**: 2025-12-03
> **Purpose**: Master index for workflow-related guidelines

This module has been split into focused sub-modules for better token efficiency and maintainability.

## Sub-Modules

| Module | Purpose | When to Load |
|--------|---------|--------------|
| [Question Handling](workflow/question-handling.md) | Processing user questions | Always |
| [Problem Solving](workflow/problem-solving.md) | Core problem-solving principles | Always |
| [Performance Analysis](workflow/performance-analysis.md) | Analyzing performance in codebases | Performance tasks |
| [GitHub Issue Guidelines](workflow/github-issue-5w1h.md) | Creating effective issues (5W1H) | Issue creation |
| [GitHub PR Guidelines](workflow/github-pr-5w1h.md) | Creating effective PRs (5W1H) | PR creation |

## Quick Reference

### Question Handling Flow
```
1. Translate → 2. Analyze → 3. Present → 4. Execute
```

### Problem-Solving Principles
- Follow procedures systematically
- Make minimal changes
- Maintain data integrity

### 5W1H Framework
- **What**: Task/problem description
- **Why**: Motivation and impact
- **Who**: Stakeholders and responsibilities
- **When**: Timeline and dependencies
- **Where**: Location and context
- **How**: Implementation approach

## Loading Rules

```yaml
# Always load
core: [question-handling, problem-solving]

# Conditional loading
performance_tasks: [performance-analysis]
github_issue: [github-issue-5w1h]
github_pr: [github-pr-5w1h]
```

## Related Modules

- [Communication](communication.md) - Language conventions
- [Git Commit Format](git-commit-format.md) - Commit message standards
- [Environment](environment.md) - Work environment settings

---
*Refactored from single 612-line file to 5 focused modules for 60-70% token savings*

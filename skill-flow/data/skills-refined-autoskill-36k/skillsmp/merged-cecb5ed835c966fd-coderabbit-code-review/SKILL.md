---
name: coderabbit-code-review
description: Use this skill for automated code review and iterative improvement in AI agent workflows, particularly after implementing new features or refactoring code.
---

# CodeRabbit Code Review

CodeRabbit is an AI-powered code review tool that helps identify race conditions, memory leaks, and security vulnerabilities. It integrates with Claude Code for autonomous review-and-fix workflows, enabling a structured approach to code quality improvement.

## Prerequisites

- **CodeRabbit CLI installed**: Install via `npm install -g @coderabbitai/cli` or follow the installation guide.
- **Authenticated**: Run `coderabbit auth login` (one-time setup).
- **Git repository**: Execute commands within a git repository to review unstaged, staged-but-uncommitted changes, and local commits.

## Quick Start

**Run review on current changes:**
```bash
coderabbit review --plain
```

**Get token-efficient summary:**
```bash
coderabbit review --prompt-only
```

**Review specific files:**
```bash
coderabbit review --files path/to/file1.ts path/to/file2.tsx
```

## AI Agent Review Workflow

### 1. Implement Code

Write the requested code or changes following project conventions.

### 2. Run CodeRabbit Review

Choose the appropriate review mode based on context:

- **Detailed feedback mode** (recommended for active development):
  ```bash
  coderabbit review --plain
  ```

- **Token-efficient mode** (for tight token budgets):
  ```bash
  coderabbit review --prompt-only
  ```

- **Review specific files** (when focusing on particular changes):
  ```bash
  coderabbit review --files path/to/file.ts
  ```

### 3. Analyze Feedback

CodeRabbit provides feedback in several categories:

- **Correctness issues**: Bugs, logic errors, type safety problems
- **Readability improvements**: Code clarity, naming, structure
- **Maintainability suggestions**: Best practices, patterns, technical debt
- **Security concerns**: Vulnerabilities, unsafe patterns
- **Performance optimizations**: Efficiency improvements

### 4. Revise Code

Apply meaningful improvements based on CodeRabbit's feedback:

- Fix correctness issues immediately.
- Address security concerns.
- Improve readability where it adds value.
- Apply maintainability suggestions that align with project patterns.

### 5. Re-review (Optional)

For significant changes or when addressing critical issues, re-run CodeRabbit to validate improvements:
```bash
coderabbit review --plain
```

## Usage Patterns

### After Feature Implementation

1. Complete the feature implementation.
2. Run `coderabbit review --plain` for comprehensive feedback.
3. Address critical and major issues.
4. Re-review if significant changes were made.

### Before PR Submission

1. Stage all changes: `git add .`
2. Run `coderabbit review --plain` to catch issues early.
3. Fix all actionable feedback.
4. Re-run review to confirm fixes.

### Exploring Unfamiliar Domains

1. Implement initial solution.
2. Run `coderabbit review --plain` to learn best practices.
3. Study feedback to understand domain conventions.

### Refactoring Existing Code

1. Make refactoring changes.
2. Run `coderabbit review --plain` to ensure no regressions.
3. Verify feedback aligns with refactoring goals.

## Command Reference

### Basic Review Commands

- **Review all uncommitted changes**:
  ```bash
  coderabbit review
  ```

- **Plain text output (detailed)**:
  ```bash
  coderabbit review --plain
  ```

- **Prompt-only output (token-efficient)**:
  ```bash
  coderabbit review --prompt-only
  ```

- **Review specific files**:
  ```bash
  coderabbit review --files path/to/file.ts
  ```

### Authentication

- **Login to CodeRabbit**:
  ```bash
  coderabbit auth login
  ```

- **Check authentication status**:
  ```bash
  coderabbit auth status
  ```

### Configuration

CodeRabbit can be configured via `.coderabbit.yaml` in the repository root. Example configuration:
```yaml
language: "en-US"
reviews:
  auto_review:
    enabled: true
```

## Best Practices

- **Token Management**: Use `--prompt-only` for tight token budgets and `--plain` during active development.
- **Feedback Analysis**: Prioritize critical issues and consider context when evaluating suggestions.
- **Iterative Improvement**: Focus on correctness and security first, and re-review after significant changes.

## When Not to Use

- **Trivial changes**: Typos, formatting-only edits.
- **Rapid prototyping**: When speed is prioritized over quality.
- **No local changes**: CodeRabbit requires unstaged, staged, or uncommitted local changes to review.

## References

- **CodeRabbit CLI Docs**: [docs.coderabbit.ai/cli](https://docs.coderabbit.ai/cli)
- **Configuration Reference**: [docs.coderabbit.ai/configuration](https://docs.coderabbit.ai/configuration)
---
name: coderabbit-cli
description: >-
  Use CodeRabbit CLI to perform automated code review and iterative improvement
  in an AI agent workflow. Use when: (1) After generating non-trivial code (new
  features, refactors, algorithms), (2) Improving code quality, maintainability,
  or readability before submission, (3) Validating code changes against best
  practices, (4) Exploring unfamiliar languages, patterns, or domains, or (5)
  Creating a self-reviewing coding loop. Requires CodeRabbit CLI installed and
  authenticated. Not for trivial changes (typos, formatting-only) or rapid
  prototyping without quality constraints.
---

# CodeRabbit CLI

Use CodeRabbit CLI to perform structured, automated code review and iterative improvement, enabling AI agents to write, review, and refine code in a tight feedback loop.

## Prerequisites

- CodeRabbit CLI installed: `npm install -g @coderabbitai/cli` or see [docs.coderabbit.ai](https://docs.coderabbit.ai)
- Authenticated: `coderabbit auth login` (one-time setup)
- Git repository: Run commands from within a git repository. CodeRabbit reviews: unstaged working-tree changes, staged-but-uncommitted changes, and local commits not yet pushed. Does not run on a clean working tree with no local changes.
- Repository context: CodeRabbit needs access to repository metadata (can be configured via `.coderabbit.yaml`)

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

Write the requested code or changes following project conventions and requirements.

### 2. Run CodeRabbit Review

Choose the appropriate review mode based on context:

**Detailed feedback mode** (recommended for active development):
```bash
coderabbit review --plain
```

**Token-efficient mode** (for tight token budgets):
```bash
coderabbit review --prompt-only
```

**Review specific files** (when focusing on particular changes):
```bash
coderabbit review --files apps/ralph-monitoring/app/routes/api.logs.ts
```

### 3. Analyze Feedback

CodeRabbit provides feedback in several categories:

- **Correctness issues**: Bugs, logic errors, type safety problems
- **Readability improvements**: Code clarity, naming, structure
- **Maintainability suggestions**: Best practices, patterns, technical debt
- **Security concerns**: Vulnerabilities, unsafe patterns
- **Performance optimizations**: Efficiency improvements

**Key principles for analyzing feedback:**
- Treat CodeRabbit as a senior reviewer: reason about suggestions, don't blindly apply them
- Prioritize correctness and security issues first
- Consider maintainability and readability improvements
- Evaluate performance suggestions in context of actual requirements
- Some suggestions may be stylistic or context-dependent

### 4. Revise Code

Apply meaningful improvements based on CodeRabbit's feedback:

- Fix correctness issues immediately
- Address security concerns
- Improve readability where it adds value
- Apply maintainability suggestions that align with project patterns
- Consider performance optimizations if they're relevant

**Document rationale** for significant changes or when choosing not to apply suggestions.

### 5. Re-review (Optional)

For significant changes or when addressing critical issues, re-run CodeRabbit to validate improvements:

```bash
coderabbit review --plain
```

This creates an iterative improvement loop until code quality meets standards.

## Usage Patterns

### After Feature Implementation

When implementing new features:

1. Complete the feature implementation
2. Run `coderabbit review --plain` for comprehensive feedback
3. Address critical and major issues
4. Re-review if significant changes were made
5. Proceed with submission when quality gates pass

### Before PR Submission

When preparing code for human review:

1. Stage all changes: `git add .`
2. Run `coderabbit review --plain` to catch issues early
3. Fix all actionable feedback
4. Re-run review to confirm fixes
5. Submit PR with confidence that basic quality checks pass

### Exploring Unfamiliar Domains

When working with new languages, frameworks, or patterns:

1. Implement initial solution
2. Run `coderabbit review --plain` to learn best practices
3. Study feedback to understand domain conventions
4. Revise code applying learned patterns
5. Use as learning tool to understand idiomatic code

### Refactoring Existing Code

When improving existing code:

1. Make refactoring changes
2. Run `coderabbit review --plain` to ensure no regressions
3. Verify feedback aligns with refactoring goals
4. Address any new issues introduced
5. Confirm code quality improved or maintained

## Command Reference

### Basic Review Commands

**Review all uncommitted changes:**
```bash
coderabbit review
```

**Plain text output (detailed):**
```bash
coderabbit review --plain
```

**Prompt-only output (token-efficient):**
```bash
coderabbit review --prompt-only
```

**Review specific files:**
```bash
coderabbit review --files path/to/file1.ts path/to/file2.tsx
```

**Review staged changes:**

```bash
git add .
coderabbit review
```

CodeRabbit automatically detects and reviews staged changes when they exist. The `coderabbit review` command will review all uncommitted changes (both staged and unstaged) by default.

### Authentication

**Login to CodeRabbit:**
```bash
coderabbit auth login
```

**Check authentication status:**
```bash
coderabbit auth status
```

### Configuration

CodeRabbit can be configured via `.coderabbit.yaml` in the repository root:

```yaml
language: "en-US"

reviews:
  review_status: false  # Suppress auto-generated status comments
  pre_merge_checks:
    docstrings:
      mode: "off"  # Disable docstring coverage checks
```

See [CodeRabbit Configuration](https://docs.coderabbit.ai/configuration) for full options.

## Integration with Development Workflow

### With Git Workflow

1. Make code changes
2. Stage changes: `git add .`
3. Run CodeRabbit review
4. Fix issues
5. Commit with confidence: `git commit -m "feat: implement feature"`
6. Push and create PR

### With AI Agent Workflows

1. Agent implements code based on requirements
2. Agent runs `coderabbit review --plain`
3. Agent analyzes feedback and identifies actionable issues
4. Agent revises code addressing feedback
5. Agent optionally re-runs review to validate fixes
6. Agent documents changes and rationale
7. Agent proceeds with next steps (tests, documentation, etc.)

## Quality Bar

When using CodeRabbit in an agent workflow:

- **Address correctness issues**: All bugs and logic errors must be fixed
- **Consider security concerns**: Security issues should be addressed or documented
- **Evaluate maintainability**: Apply suggestions that align with project patterns
- **Reason about feedback**: Don't blindly apply all suggestions; understand intent
- **Document decisions**: When choosing not to apply suggestions, note rationale

## When Not to Use

- **Trivial changes**: Typos, formatting-only edits, simple renames
- **Rapid prototyping**: When speed is more important than quality
- **Repository not initialized**: CodeRabbit needs git context
- **No local changes**: Nothing to review if working tree is clean (no unstaged, staged, or uncommitted local changes)

## Best Practices

### Token Management

- Use `--prompt-only` when operating under tight token budgets
- Use `--plain` during active development for detailed feedback
- Focus on actionable feedback rather than reading all suggestions

### Feedback Analysis

- Prioritize critical and major issues
- Group similar suggestions for efficient addressing
- Consider context when evaluating stylistic suggestions
- Some suggestions may conflict with project conventions

### Iterative Improvement

- Don't try to address all feedback in one pass
- Focus on correctness and security first
- Re-review after significant changes
- Use feedback as learning opportunity

## Reference Documentation

- **CodeRabbit CLI Docs**: [docs.coderabbit.ai/cli](https://docs.coderabbit.ai/cli)
- **Configuration Reference**: [docs.coderabbit.ai/configuration](https://docs.coderabbit.ai/configuration)
- **Review Guidelines**: See [references/cli-commands.md](references/cli-commands.md) for complete command reference

---
name: code-reviewer
description: Comprehensive code review for quality, architecture, and performance. Use when reviewing PRs, auditing code quality, checking coding standards, evaluating design patterns, identifying performance bottlenecks, or analyzing technical debt. Triggers on "review", "audit", "analyze code", "check quality", "code smell".
---

# Code Reviewer

Perform thorough code reviews covering quality, architecture, and performance aspects.

## When to Use

- Reviewing pull requests or code changes
- Auditing codebase quality and maintainability
- Evaluating architecture and design decisions
- Identifying performance issues and bottlenecks
- Checking adherence to coding standards
- Finding code smells and technical debt

## Review Process

### 1. Understand Context

Before reviewing, gather context:
- What is the purpose of this code/change?
- What are the project's conventions? (check CLAUDE.md, .eslintrc, etc.)
- Are there existing patterns to follow?

### 2. Quality Review

Check for:
- **Readability**: Clear naming, appropriate comments, logical structure
- **Maintainability**: Single responsibility, DRY principle, low coupling
- **Error handling**: Proper try/catch, meaningful error messages
- **Edge cases**: Null checks, boundary conditions, empty states
- **Code smells**: Long methods, deep nesting, magic numbers

### 3. Architecture Review

Evaluate:
- **Design patterns**: Appropriate use, consistency with codebase
- **Dependencies**: Minimal coupling, clear interfaces
- **Modularity**: Components have clear boundaries and responsibilities
- **Scalability**: Can this handle growth without major rewrites?
- **Testability**: Is the code easy to unit test?

### 4. Performance Review

Identify:
- **Algorithmic efficiency**: Time/space complexity concerns
- **Memory management**: Leaks, unnecessary allocations
- **Render performance**: Unnecessary re-renders (React), DOM thrashing
- **Network efficiency**: N+1 queries, missing caching, payload sizes
- **Resource cleanup**: Event listeners, subscriptions, intervals

## Output Format

Structure your review as:

```markdown
## Code Review: [File/Component Name]

### Summary
[1-2 sentence overview of the review findings]

### Critical Issues
[Must fix before merge - bugs, security issues, data loss risks]

### Recommendations
[Should fix - quality, performance, maintainability improvements]

### Suggestions
[Nice to have - style preferences, minor optimizations]

### Positive Highlights
[Good patterns worth noting for team learning]
```

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| Critical | Bugs, security vulnerabilities, data corruption risk | Block merge |
| High | Performance issues, maintainability problems | Should fix |
| Medium | Code smells, minor inefficiencies | Recommend fix |
| Low | Style preferences, nitpicks | Optional |

## Review Checklist

See [CHECKLIST.md](CHECKLIST.md) for the complete review checklist.

## Examples

See [EXAMPLES.md](EXAMPLES.md) for sample reviews demonstrating proper format and tone.
